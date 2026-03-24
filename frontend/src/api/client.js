import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  timeout: 15000,
});

export const getStats = async () => {
  const { data } = await api.get("/get-stats");
  return data;
};

export const getRiskPrediction = async () => {
  const { data } = await api.get("/predict");
  return data;
};

export const askAssistant = async (question) => {
  const { data } = await api.post("/ask", { question });
  return data;
};
