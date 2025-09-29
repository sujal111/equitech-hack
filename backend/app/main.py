# incident_graph_with_llm.py
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
import openai

# ---- CONFIG ----
config_list = [
    {
        "model": "gpt-4-32k",
        "api_key": "",
        "azure_endpoint": "",
        "api_type": "azure",
        "api_version": "2023-07-01-preview"
    }
]

# Initialize OpenAI client with Azure setup
cfg = config_list[0]
openai.api_type = cfg["api_type"]
openai.api_base = cfg["azure_endpoint"]
openai.api_version = cfg["api_version"]
openai.api_key = cfg["api_key"]

# ---- STATE ----
class IncidentState(TypedDict, total=False):
    raw_events: List[Dict[str, Any]]
    normalized_events: List[Dict[str, Any]]
    candidate_incidents: List[Dict[str, Any]]
    correlated_incident: Dict[str, Any]
    enrichment: Dict[str, Any]
    priority: Dict[str, Any]
    actions_taken: List[Dict[str, Any]]
    analyst_decision: Dict[str, Any]
    logs: List[str]

# ---- NODES ----
def ingest_node(state: IncidentState):
    raw = state.get("raw_events", [])
    return {"raw_events": raw, "logs": state.get("logs", []) + [f"ingested:{len(raw)}"]}

def parse_node(state: IncidentState):
    raw = state.get("raw_events", [])
    normalized = []
    for e in raw:
        normalized.append({
            "ts": e.get("timestamp"),
            "src_ip": e.get("src") or e.get("source_ip"),
            "dst_ip": e.get("dst") or e.get("dest_ip"),
            "user": e.get("user"),
            "event_type": e.get("type"),
            "message": e.get("message"),
            "raw": e
        })
    return {"normalized_events": normalized, "logs": state.get("logs", []) + [f"parsed:{len(normalized)}"]}

def feature_extract_node(state: IncidentState):
    norm = state.get("normalized_events", [])
    features = []
    for e in norm:
        features.append({
            "ts": e["ts"],
            "src_ip": e["src_ip"],
            "dst_ip": e["dst_ip"],
            "event": e,
        })
    return {"candidate_incidents": [{"features": features}], "logs": state.get("logs", []) + ["features_extracted"]}

def signature_matcher_node(state: IncidentState):
    candidates = state.get("candidate_incidents", [])
    for cand in candidates:
        cand["sig_hits"] = []
    return {"candidate_incidents": candidates, "logs": state.get("logs", []) + ["sig_checked"]}

def anomaly_detector_node(state: IncidentState):
    candidates = state.get("candidate_incidents", [])
    updated = []
    for cand in candidates:
        prompt = f"""
        You are a SOC analyst. Given the following normalized events:
        {cand['features']}

        Task: Determine if this activity looks anomalous or malicious.
        Return JSON with fields: anomaly_score (0-1), explanation.
        """
        try:
            resp = openai.ChatCompletion.create(
                engine=cfg["model"],  # use "engine" for Azure deployments
                messages=[{"role": "system", "content": "You are an expert SOC analyst."},
                          {"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=300
            )
            content = resp["choices"][0]["message"]["content"]
            cand["anomaly_llm_raw"] = content
        except Exception as e:
            cand["anomaly_llm_raw"] = f"Error: {e}"
        updated.append(cand)

    return {"candidate_incidents": updated, "logs": state.get("logs", []) + ["anomaly_scored_llm"]}

def correlator_node(state: IncidentState):
    candidates = state.get("candidate_incidents", [])
    correlated = {
        "id": "incident-001",
        "events": candidates[0].get("features", []) if candidates else [],
        "combined_score": 0.9,
        "sig_hits": sum(len(c.get("sig_hits", [])) for c in candidates),
    }
    return {"correlated_incident": correlated, "logs": state.get("logs", []) + ["correlated"]}

def enricher_node(state: IncidentState):
    enrich = {"ip_reputation": {"192.0.2.1": "suspicious"}}
    return {"enrichment": enrich, "logs": state.get("logs", []) + ["enriched"]}

def prioritizer_node(state: IncidentState):
    return {"priority": {"priority_score": 1.8, "tpep": "P1"}, "logs": state.get("logs", []) + ["prioritized"]}

def responder_node(state: IncidentState):
    return {"actions_taken": [{"action": "isolate_host", "status": "ok"}], "logs": state.get("logs", []) + ["responded"]}

def notifier_node(state: IncidentState):
    return {"logs": state.get("logs", []) + ["notified"], "ticket": {"ticket_id": "INC123"}}

def supervisor_node(state: IncidentState):
    return {"analyst_decision": {"verdict": "investigate"}, "logs": state.get("logs", []) + ["supervised"]}

def feedback_node(state: IncidentState):
    return {"logs": state.get("logs", []) + ["feedback_saved"]}

# ---- GRAPH BUILDER ----
from langgraph.graph import StateGraph

def build_incident_graph():
    builder = StateGraph(IncidentState)
    builder.add_sequence([
        ingest_node,
        parse_node,
        feature_extract_node,
        signature_matcher_node,
        anomaly_detector_node,  # now LLM-powered
        correlator_node,
        enricher_node,
        prioritizer_node,
        responder_node,
        notifier_node,
        supervisor_node,
        feedback_node
    ])
    builder.add_edge(START, "ingest_node")
    return builder

if __name__ == "__main__":
    graph = build_incident_graph()
    initial_state = IncidentState(raw_events=[{"timestamp":"2025-09-30T12:00Z","src":"192.0.2.1","message":"Unusual outbound connection"}])
    result = graph.run(initial_state)
    print("Logs:", result.get("logs"))
    print("Incident:", result.get("correlated_incident"))
