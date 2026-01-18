    
    
    <template>
  <!-- CHANGE 1: lock layout to viewport + hide global scroll -->
  <div class="h-screen w-full bg-[#0b1224] text-white overflow-hidden flex flex-col font-sans">

    <!-- NAVBAR (fixed top) -->
    <nav class="w-full fixed top-0 left-0 z-50 bg-[#0b1224] border-b border-slate-800">
      <!-- CHANGE 2: slightly reduced padding -->
      <div class="max-w-7xl mx-auto flex justify-between items-center px-6 md:px-12 py-4">
        <div class="flex items-center gap-3">
          <div
            class="bg-blue-600 w-10 h-10 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
            <span class="text-white font-bold text-lg">MPT</span>
          </div>
          <router-link
            to="/"
            class="text-sm font-medium text-slate-300 hover:text-white transition">
             <h1 class="text-xl font-bold tracking-tight text-white">Math pour tous</h1>
          </router-link>
         
        </div>

        <div class="flex items-center gap-6">
          <router-link
            to="/login"
            class="text-sm font-medium text-slate-300 hover:text-white transition">
            Se connecter
          </router-link>
          <router-link
            to="/register"
            class="px-6 py-2 bg-blue-500 hover:bg-blue-600 rounded-full font-bold text-sm transition-all shadow-lg">
            <span class="text-white">S'inscrire</span>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- SCROLLABLE CONTENT AREA -->
    <!-- CHANGE 3: scroll only here + spacing for fixed navbar/footer -->
    
    <main class="flex-grow flex items-center justify-center px-6 min-h-0">
      <div class="w-full max-w-md bg-[#161f32]/60 backdrop-blur-xl rounded-[2.5rem] border border-slate-800 p-10 shadow-2xl">
        
        <div class="text-center mb-8">
          <h2 class="text-3xl font-black mb-2 tracking-tight">Bon retour !</h2>
          <p class="text-slate-400 text-sm font-medium">Connecte-toi pour continuer ton apprentissage</p>
        </div>

       <form class="space-y-5" @submit.prevent="submitLogin">
          <div class="space-y-1.5">
            <label class="block text-[10px] font-bold text-slate-500 ml-1 uppercase tracking-widest">Email</label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs">✉️</span>
              <input type="email" v-model="form.email" placeholder="ton@email.com" class="w-full bg-[#0b1224]/50 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition placeholder:text-slate-600" />
            </div>
          </div>

          <div class="space-y-1.5">
            <div class="flex justify-between items-center px-1">
              <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest">Mot de passe</label>
            </div>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs">🔒</span>
              <input type="password" v-model="form.password" placeholder="••••••••" class="w-full bg-[#0b1224]/50 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition placeholder:text-slate-600" />
            </div>
          </div>
        <a href="#" class="text-[10px] text-blue-400 hover:underline">Oublié ?</a>
          <button type="submit" class="w-full py-4 mt-4 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 font-bold text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all">
            Se connecter
          </button>
        </form>

        <p class="text-center text-sm text-slate-400 mt-8 font-medium">
          Nouveau ici ?
          <router-link to="/register" class="text-blue-400 font-bold hover:underline ml-1">Créer un compte</router-link>
        </p>
      </div>
    </main>

    <!-- FOOTER (fixed bottom) -->
    <footer class="w-full fixed bottom-0 left-0 border-t border-slate-800 bg-[#0b1224]">
      <!-- CHANGE 7: reduced padding -->
      <div class="max-w-7xl mx-auto px-6 md:px-12 py-3 text-center text-sm text-slate-400">
        Projet interne <span class="text-white font-semibold">2025–2026</span> · Projet IA
      </div>
    </footer>

  </div>
</template>
<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { loginUser } from "../services/authService"

const router = useRouter()

const form = ref({
  email: "",
  password: ""
})

const error = ref("")
const loading = ref(false)

const submitLogin = async () => {
  error.value = ""
  loading.value = true

  try {
    const res = await loginUser(form.value)

    // Stockage JWT
    localStorage.setItem("token", res.data.access_token)
    localStorage.setItem("user", JSON.stringify(res.data.user))

    router.push("/chat")
  } catch (err) {
    error.value = "Email ou mot de passe incorrect"
  } finally {
    loading.value = false
  }
}
</script>
