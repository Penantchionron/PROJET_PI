import { createRouter, createWebHistory } from "vue-router"

import LandingPage from "../pages/Landing.vue"
import LoginPage from "../pages/Login.vue"
import RegisterPage from "../pages/Register.vue"
import ChatPage from "../pages/Chat.vue"
import AdminPage from "../pages/Admin.vue"

const routes = [
  { path: "/", component: LandingPage },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },

  {
    path: "/chat",
    component: ChatPage,
    meta: { auth: true }
  },

  {
    path: "/admin",
    component: AdminPage,
    meta: { auth: true, admin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🔐 GUARD JWT
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token")
  const user = JSON.parse(localStorage.getItem("user"))

  if (to.meta.auth && !token) {
    return next("/login")
  }

  if (to.meta.admin && user?.role !== "admin") {
    return next("/chat")
  }

  next()
})

export default router
