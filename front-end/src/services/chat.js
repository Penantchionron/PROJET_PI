import api from "../services/api"

export const fetchChats = () => api.get("/api/chat")
export const createChat = (title = "Nouveau chat") =>
  api.post("/api/chat", { title })

export const fetchMessages = (chatId) =>
  api.get(`/api/chat/${chatId}/messages`)

export const sendMessage = (chatId, content) =>
  api.post(`/api/chat/${chatId}/message`, { content })
