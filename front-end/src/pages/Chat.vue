
<template>
  <div class="fixed inset-0 flex bg-[#0b1224] text-slate-100 overflow-hidden">
    
    <!-- Sidebar -->
    <aside class="hidden md:flex w-72 flex-col bg-[#121a2f] border-r border-slate-800">
      <div class="p-4 flex-shrink-0">
        <button
          @click="newChat"
          class="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 py-3 text-sm font-semibold hover:opacity-90 transition"
        >
          ＋ Nouveau chat
        </button>
      </div>

      <div class="flex-1 min-h-0 overflow-y-auto px-3 space-y-2 scrollbar-thin scrollbar-thumb-slate-700">
        <div
          v-for="chat in chats"
          :key="chat.id"
          @click="selectChat(chat.id)"
          :class="[ 'px-3 py-2 rounded-lg text-sm cursor-pointer truncate transition',
                    currentChatId === chat.id
                      ? 'bg-blue-600/20 border border-blue-500/50 text-blue-400'
                      : 'bg-[#161f32] hover:bg-[#1c2744]' ]"
        >
          {{ chat.title || 'Nouveau chat' }}
        </div>
      </div>

      <div class="p-4 border-t border-slate-800 flex-shrink-0 space-y-2">
        <button class="w-full text-left text-sm text-slate-400 hover:text-white transition flex items-center gap-2 p-2 rounded-lg hover:bg-slate-800">
          ⚙️ Paramètres
        </button>
        <button @click="handleLogout" class="w-full text-left text-sm text-red-400 hover:text-red-300 transition flex items-center gap-2 p-2 rounded-lg hover:bg-red-400/10">
          🚪 Déconnexion
        </button>
      </div>
    </aside>

    <!-- Main chat area -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <header class="h-16 flex items-center px-6 border-b border-slate-800 flex-shrink-0 bg-[#0b1224]/50 backdrop-blur-md">
        <div class="flex items-center gap-3" v-if="user">
          <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-lg font-bold shadow-lg shadow-blue-500/20">
            {{ user.prenom?.[0] }}{{ user.nom?.[0] }}
          </div>
          <div>
            <p class="text-sm font-semibold leading-none">{{ user.prenom }} {{ user.nom }}</p>
            <p class="text-xs text-slate-400 mt-1">Niveau : <span class="text-blue-400 font-medium">{{ user.niveau }}</span></p>
          </div>
        </div>
      </header>

      <!-- Messages container -->
      <div class="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin" ref="scrollContainer">
        <div v-for="msg in messages" :key="msg.id" class="max-w-4xl mx-auto w-full">

          <!-- IA message -->
          <div v-if="msg.role === 'assistant'" class="flex items-start gap-3">
            <div class="w-8 h-8 rounded bg-gradient-to-br from-blue-600 to-cyan-500 flex-shrink-0 flex items-center justify-center text-[10px] font-bold shadow-md">IA</div>
            <div class="bg-[#161f32] border border-slate-800 rounded-2xl px-4 py-3 text-sm max-w-[85%] text-slate-200 leading-relaxed shadow-sm">
              
              <!-- Title -->
              <h2 class="text-lg font-bold text-blue-400 mb-2">{{ extractTitle(msg.content) }}</h2>

              <!-- Sections -->
              <div v-for="(content, key) in parseIAResponse(msg.content)" :key="key" class="mb-3">
                <h3 class="font-semibold text-cyan-400 mb-1">{{ key }} :</h3>

                <template v-if="key === 'EXERCICE' || key === 'CORRECTION'">
                  <ol class="list-decimal list-inside ml-4 space-y-1 markdown-body">
                    <li v-for="item in splitLines(content)" :key="item" v-html="renderMarkdown(item)"></li>
                  </ol>
                </template>

                <template v-else>
                  <div v-html="renderMarkdown(content)" class="markdown-body"></div>
                </template>
              </div>

            </div>
          </div>

          <!-- User message -->
          <div v-else class="flex justify-end">
            <div class="bg-blue-600 rounded-2xl px-4 py-3 text-sm max-w-[80%] text-white shadow-lg shadow-blue-500/10">
              {{ msg.content }}
            </div>
          </div>

        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="flex items-start gap-3 max-w-4xl mx-auto w-full animate-pulse">
          <div class="w-8 h-8 rounded bg-slate-700 flex-shrink-0 flex items-center justify-center text-[10px]">...</div>
          <div class="bg-[#161f32]/50 border border-slate-800 rounded-2xl px-4 py-3 text-xl text-white text-slate-500 italic">
            L'IA prépare sa réponse...
          </div>
        </div>

        <!-- Empty state -->
        <div v-if="messages.length === 0 && !isLoading" class="h-full flex flex-col items-center justify-center text-slate-500 space-y-4">
          <div class="text-4xl">📐</div>
          <p class="text-lg font-light italic">Pose-moi une question sur ton cours de maths !</p>
        </div>
      </div>

      <!-- Input -->
      <div class="border-t border-slate-800 bg-[#0b1224] px-4 py-4">
        <div class="max-w-3xl mx-auto">
          <div class="flex items-end gap-2 bg-[#161f32] rounded-2xl border border-slate-700 px-3 py-2 focus-within:border-blue-500 transition-all duration-200 shadow-inner">
            
            <label class="cursor-pointer text-slate-400 hover:text-white p-2 transition flex-shrink-0">
              📎
              <input type="file" class="hidden" multiple @change="handleFileUpload" />
            </label>

            <textarea
              ref="inputRef"
              v-model="messageInput"
              rows="1"
              @input="autoResize"
              @keydown.enter.exact.prevent="send"
              :disabled="isLoading"
              placeholder="Écris ta question ici…"
              class="flex-1 resize-none bg-transparent outline-none text-sm py-2 max-h-40 disabled:opacity-50"
            ></textarea>

            <button
              @click="send"
              :disabled="!messageInput.trim() || isLoading"
              class="p-2 text-blue-400 hover:text-blue-300 disabled:opacity-20 transition-colors"
            >
              <span v-if="!isLoading">➤</span>
              <span v-else class="block w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></span>
            </button>
          </div>

          <div v-if="files.length" class="mt-2 flex flex-wrap gap-2">
            <div
              v-for="(file, index) in files"
              :key="index"
              class="flex items-center gap-2 bg-[#1c2744] border border-slate-700 rounded-xl px-3 py-1 text-xs"
            >
              📄 {{ file.name }}
              <button @click="removeFile(index)" class="text-red-400 hover:text-red-300">✕</button>
            </div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"
import { fetchChats, createChat, fetchMessages, sendMessage } from "../services/chat"

// Markdown + KaTeX
import MarkdownIt from 'markdown-it'
import mk from 'markdown-it-katex'
import 'katex/dist/katex.min.css'

const md = new MarkdownIt().use(mk)

// STATE
const router = useRouter()
const user = ref(null)
const chats = ref([])
const currentChatId = ref(null)
const messages = ref([])
const messageInput = ref("")
const isLoading = ref(false)
const inputRef = ref(null)
const scrollContainer = ref(null)
const files = ref([])

// LIFECYCLE
onMounted(async () => {
  try {
    const userRes = await api.get("/api/auth/me")
    user.value = userRes.data
    
    const chatRes = await fetchChats()
    chats.value = chatRes.data || []

    if (chats.value.length > 0) {
      currentChatId.value = chats.value[0].id
      await loadMessages()
    } else {
      await newChat()
    }
  } catch (err) {
    console.error("Erreur initialisation :", err)
    router.push("/login")
  }
})

// ACTIONS
const scrollToBottom = async () => {
  await nextTick()
  if (scrollContainer.value) scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
}

const selectChat = async (id) => {
  if (isLoading.value) return
  currentChatId.value = id
  await loadMessages()
}

const newChat = async () => {
  try {
    const res = await createChat()
    chats.value.unshift(res.data)
    currentChatId.value = res.data.id
    messages.value = []
  } catch (err) {
    console.error("Erreur création chat:", err)
  }
}

const loadMessages = async () => {
  if (!currentChatId.value) return
  try {
    const res = await fetchMessages(currentChatId.value)
    messages.value = res.data || []
    scrollToBottom()
  } catch (err) {
    console.error("Erreur chargement messages:", err)
  }
}

const send = async () => {
  if (!messageInput.value.trim() || !currentChatId.value || isLoading.value) return

  const content = messageInput.value
  messageInput.value = ""
  isLoading.value = true
  if (inputRef.value) inputRef.value.style.height = 'auto'

  try {
    const res = await sendMessage(currentChatId.value, content)
    messages.value = res.data
    scrollToBottom()

    const chatRes = await fetchChats()
    chats.value = chatRes.data || []
  } catch (err) {
    console.error("Erreur envoi message:", err)
  } finally {
    isLoading.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem("token")
  delete api.defaults.headers.common["Authorization"]
  router.push("/login")
}

const autoResize = () => {
  const el = inputRef.value
  if (!el) return
  el.style.height = "auto"
  el.style.height = el.scrollHeight + "px"
}

const handleFileUpload = (event) => {
  const newFiles = Array.from(event.target.files)
  files.value.push(...newFiles)
}

const removeFile = (index) => {
  files.value.splice(index, 1)
}

// UTILITIES
const renderMarkdown = (text) => {
  if (!text) return ''
  return md.render(text)
}

const parseIAResponse = (text) => {
  const sections = {}
  const regex = /(EXPLICATION|EXEMPLE|EXERCICE|CORRECTION) ?:?/g
  let lastIndex = 0
  let match
  let currentSection = null
  while ((match = regex.exec(text)) !== null) {
    if (currentSection) sections[currentSection] = text.slice(lastIndex, match.index).trim()
    currentSection = match[1]
    lastIndex = regex.lastIndex
  }
  if (currentSection) sections[currentSection] = text.slice(lastIndex).trim()
  return sections
}

const splitLines = (text) => text.split(/\n|;/).map(s => s.trim()).filter(Boolean)

const extractTitle = (text) => {
  const idx = text.indexOf("EXPLICATION")
  if (idx > 0) return text.slice(0, idx).replace(":", "").trim()
  return "Réponse IA"
}
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 20px;
}
.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #1e293b;
  border-radius: 10px;
}
.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #334155;
}
.markdown-body p {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}
.markdown-body ol, .markdown-body ul {
  padding-left: 1.25rem;
}
.markdown-body code {
  background: #1c2744;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: monospace;
}
</style>
