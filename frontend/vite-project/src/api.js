import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export const createIncident = async (incident) => {
  const response = await API.post("/incident", incident);
  return response.data;
};
