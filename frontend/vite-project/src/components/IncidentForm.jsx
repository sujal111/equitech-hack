// import { useState } from "react";
// import { createIncident } from "../api";

// export default function IncidentForm({ onNewIncident }) {
//   const [title, setTitle] = useState("");
//   const [description, setDescription] = useState("");
//   const [severity, setSeverity] = useState("Low");

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     const res = await createIncident({ title, description, severity });
//     onNewIncident(res.data);
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
//       <input placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
//       <select value={severity} onChange={(e) => setSeverity(e.target.value)}>
//         <option>Low</option>
//         <option>Medium</option>
//         <option>High</option>
//       </select>
//       <button type="submit">Create Incident</button>
//     </form>
//   );
// }




import { useState } from "react";
import { createIncident } from "../api";

export default function IncidentForm({ onNewIncident }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState("Low");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await createIncident({ title, description, severity });
      onNewIncident(res.data);
      setTitle("");
      setDescription("");
      setSeverity("Low");
    } catch (err) {
      alert("Failed to create incident");
    }
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h2>Create New Incident</h2>
      <input
        className="input"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <textarea
        className="textarea"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />
      <select
        className="select"
        value={severity}
        onChange={(e) => setSeverity(e.target.value)}
      >
        <option>Low</option>
        <option>Medium</option>
        <option>High</option>
      </select>
      <button className="button" type="submit">
        Create Incident
      </button>
    </form>
  );
}

