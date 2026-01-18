<template>
  <!-- CHANGE 1: lock layout to viewport + hide global scroll -->
  <div class="h-screen w-full bg-[#0b1224] text-white overflow-hidden flex flex-col font-sans ">

    <!-- NAVBAR (fixed top) -->
    <nav class="w-full fixed top-0 left-0 z-50 bg-[#0b1224] border-b border-slate-800">
      <!-- CHANGE 2: slightly reduced padding -->
      <div class="max-w-7xl mx-auto flex justify-between items-center px-6 md:px-12 py-4">
        <div class="flex items-center gap-3">
          <div
            class="bg-blue-600 w-10 h-10 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
            <span class="text-white font-bold text-lg">MPT</span>
          </div>
          <h1 class="text-xl font-bold tracking-tight">Math pour tous</h1>
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
    <main class="flex-1 overflow-y-auto pt-20 pb-16 bg-[#0b1224]">
    
      <!-- HERO -->
      <section class="flex items-center justify-center text-center">
        <div class="max-w-5xl px-0">

          <!-- CHANGE 4: reduced margins -->
          <h2
            class="text-4xl sm:text-5xl md:text-7xl font-black mb-4 leading-tight tracking-tight">
            Apprendre les
            <span
              class="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400">
              Maths
            </span>
            <br />
            avec l'IA
          </h2>

          <p class="text-slate-400 max-w-2xl mx-auto text-lg mb-6">
            Un assistant pédagogique intelligent adapté aux élèves de la 6e à la 3e
            selon le programme ivoirien.
          </p>

          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <router-link
              to="/register"
              class="px-10 py-4 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-xl shadow-xl shadow-blue-500/20 transition-all">
              <span class="text-white">Commencerz maintenant →</span>
            </router-link>

            <router-link
              to="/login"
              class="px-10 py-4 bg-slate-800/50 border border-slate-700 text-white font-bold rounded-xl hover:bg-slate-800 transition-all">
              Se connecter
            </router-link>
          </div>
        </div>
      </section>

      <!-- FEATURES -->
      <!-- CHANGE 5: reduced vertical padding -->
      <section class="w-full py-8">
        <div class="max-w-7xl mx-auto px-6 md:px-12">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

            <!-- CHANGE 6: smaller padding + radius -->
            <div class="bg-[#161f32] p-6 rounded-xl border border-slate-800 text-center">
              <div class="text-2xl mb-3">📘</div>
              <h3 class="text-lg font-bold mb-2">Explications simples</h3>
              <p class="text-slate-400 text-sm">
                Des réponses claires et adaptées à ton niveau.
              </p>
            </div>

            <div class="bg-[#161f32] p-6 rounded-xl border border-slate-800 text-center">
              <div class="text-2xl mb-3">🧠</div>
              <h3 class="text-lg font-bold mb-2">IA pédagogique</h3>
              <p class="text-slate-400 text-sm">
                Entraîné pour l'apprentissage interactif.
              </p>
            </div>

            <div class="bg-[#161f32] p-6 rounded-xl border border-slate-800 text-center">
              <div class="text-2xl mb-3">✏️</div>
              <h3 class="text-lg font-bold mb-2">Exercices corrigés</h3>
              <p class="text-slate-400 text-sm">
                Pratique et reçois une correction détaillée.
              </p>
            </div>

          </div>
        </div>
      </section>

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
