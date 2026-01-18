// src/services/api.js
// src/services/api.js
import axios from "axios"

const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 60000 // On autorise jusqu'à 60 secondes pour les réponses de l'IA
})
// Intercepteur JWT
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

export default api
