<template>
  <!-- ROOT FIXED -->
  <div
    class="fixed inset-0 flex bg-[#0b1224] text-slate-100
           overflow-hidden overflow-x-hidden"
  >

    <!-- SIDEBAR -->
    <aside
      class="hidden md:flex w-72 flex-col bg-[#121a2f]
             border-r border-slate-800
             overflow-x-hidden"
    >
      <!-- New Chat -->
      <div class="p-4 flex-shrink-0">
        <button
          class="w-full flex items-center justify-center gap-2
                 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500
                 py-3 text-sm font-semibold hover:opacity-90 transition"
        >
          Dashboard
        </button>
        
      </div>

      <!-- Scrollable history -->
      <div
        class="flex-1 min-h-0 overflow-y-auto overflow-x-hidden
               px-3 space-y-2 scrollbar-thin scrollbar-thumb-slate-700"
      >
        <div
          v-for="i in 2"
          :key="i"
          class="px-3 py-2 rounded-lg text-sm bg-[#161f32]
                 hover:bg-[#1c2744] cursor-pointer truncate"
        >
          Statistiques {{ i }}
        </div>
      </div>

      <!-- Settings -->
<!-- Settings & Logout -->
<div class="p-4 border-t border-slate-800 flex-shrink-0 space-y-2">

  <button
    class="w-full text-left text-sm text-slate-400
           hover:text-white transition flex items-center gap-2"
  >
    ⚙️ Paramètres
  </button>

  <button
    class="w-full text-left text-sm text-red-400
           hover:text-red-300 transition flex items-center gap-2"
  >
    🚪 Déconnexion
  </button>

</div>

    </aside>

    <!-- MAIN -->
    <main
      class="flex-1 flex flex-col min-w-0
             overflow-hidden overflow-x-hidden"
    >
      <!-- Header -->
      <header
        class="h-16 flex items-center px-6
               border-b border-slate-800 flex-shrink-0"
      >
        <div class="flex items-center px-12 gap-12">
        <button
          class="w-full flex items-center justify-center gap-4
                 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500
                 py-3 text-sm font-semibold hover:opacity-90 transition"
        >
          Utilisateurs        </button>
          <button
          class="w-full flex items-center justify-center gap-4
                 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500
                 py-3 text-sm font-semibold hover:opacity-90 transition"
        >
          Exercices
        </button>
          <button
          class="w-full flex items-center justify-center gap-4
                 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500
                 py-3 text-sm font-semibold hover:opacity-90 transition"
        >
          Chiffres
        </button>
        </div>
      </header>
    </main>
  </div>
</template>


<script setup>

</script>
