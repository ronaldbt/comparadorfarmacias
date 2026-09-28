<script setup lang="ts">
const open = ref(false)
const cityOpen = ref(false)
const categoryOpen = ref(false)
const city = ref('Santiago')
const searchCategory = ref('Todas')
const route = useRoute()
const draft = ref(typeof route.query.q === 'string' ? route.query.q : '')
const cityBox = ref<HTMLElement | null>(null)
const categoryBox = ref<HTMLElement | null>(null)
const { query } = useCatalog()
const anchoPagina = computed(() => route.path === '/remedios' ? 'max-w-[1480px]' : 'max-w-6xl')

const cities = ['Santiago', 'Bogotá', 'Ciudad de México', 'Madrid', 'Buenos Aires']
const searchCategories = ['Todas', 'Medicamentos', 'Vitaminas', 'Cuidado personal', 'Bebés']

const links = [
  { label: 'Remedios', to: '/remedios' },
  { label: 'Comparar precios', to: '/comparar' },
  { label: 'Comprar por categorías', to: '/#categorias', icon: true },
  { label: 'Menos de $1.000', to: '/#productos' },
  { label: 'Más vendidos', to: '/#productos', dot: true },
  { label: 'Novedades', to: '/#productos' },
  { label: 'Ofertas', to: '/#productos' },
  { label: 'Cuidado personal', to: '/#categorias' },
  { label: 'Vitaminas y suplementos', to: '/#categorias' }
]

watch(() => route.query.q, (value) => {
  if (typeof value === 'string') draft.value = value
})

function submitSearch() {
  const term = draft.value.trim()
  query.value = term
  open.value = false
  categoryOpen.value = false
  if (term.length < 2) return
  navigateTo({ path: '/comparar', query: { q: term } })
}

function chooseCity(name: string) {
  city.value = name
  cityOpen.value = false
}

function chooseCategory(name: string) {
  searchCategory.value = name
  categoryOpen.value = false
}

function onDocumentClick(event: MouseEvent) {
  const target = event.target as Node
  if (cityBox.value && !cityBox.value.contains(target)) cityOpen.value = false
  if (categoryBox.value && !categoryBox.value.contains(target)) categoryOpen.value = false
}

onMounted(() => document.addEventListener('click', onDocumentClick))
onBeforeUnmount(() => document.removeEventListener('click', onDocumentClick))
</script>

<template>
  <header>
    <div class="sticky top-0 z-40">
      <p class="bg-forest-deep px-4 py-2 text-center text-[11px] text-white/90 sm:text-xs">
        Envío gratis en compras sobre $25.000
      </p>

      <div class="bg-forest text-white">
        <div class="mx-auto flex items-center gap-3 px-4 py-3 sm:px-6" :class="anchoPagina">
          <NuxtLink to="/" class="shrink-0 text-xl font-semibold tracking-tight" aria-label="Salvia, inicio">
            Salvia
          </NuxtLink>

          <div ref="cityBox" class="relative hidden lg:block">
            <button
              type="button"
              class="flex items-center gap-2 rounded-full border border-white/25 px-3 py-2 text-sm"
              :aria-expanded="cityOpen"
              @click="cityOpen = !cityOpen"
            >
              <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path stroke-linecap="round" d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z" />
                <circle cx="12" cy="10" r="2.2" />
              </svg>
              <span class="text-left leading-tight">
                <span class="block text-[10px] text-white/70">Entregar en</span>
                <span class="block text-sm">{{ city }}</span>
              </span>
              <svg viewBox="0 0 24 24" class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path stroke-linecap="round" d="m6 9 6 6 6-6" />
              </svg>
            </button>
            <ul v-if="cityOpen" class="absolute left-0 top-full z-20 mt-2 w-52 overflow-hidden rounded-2xl bg-white py-1 text-ink shadow-card">
              <li v-for="name in cities" :key="name">
                <button type="button" class="block w-full px-4 py-2 text-left text-sm hover:bg-mist" @click="chooseCity(name)">
                  {{ name }}
                </button>
              </li>
            </ul>
          </div>

          <form class="hidden min-w-0 flex-1 items-center rounded-full bg-white p-1 text-ink md:flex" @submit.prevent="submitSearch">
            <div ref="categoryBox" class="relative shrink-0">
              <button type="button" class="flex items-center gap-1 rounded-full px-3 py-2 text-sm" :aria-expanded="categoryOpen" @click="categoryOpen = !categoryOpen">
                {{ searchCategory }}
                <svg viewBox="0 0 24 24" class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                  <path stroke-linecap="round" d="m6 9 6 6 6-6" />
                </svg>
              </button>
              <ul v-if="categoryOpen" class="absolute left-0 top-full z-20 mt-2 w-48 overflow-hidden rounded-2xl bg-white py-1 shadow-card">
                <li v-for="name in searchCategories" :key="name">
                  <button type="button" class="block w-full px-4 py-2 text-left text-sm hover:bg-mist" @click="chooseCategory(name)">
                    {{ name }}
                  </button>
                </li>
              </ul>
            </div>
            <input
              v-model="draft"
              type="search"
              placeholder="Busca medicamentos, productos de salud..."
              class="min-w-0 flex-1 bg-transparent px-2 text-sm outline-none placeholder:text-mute"
              aria-label="Buscar medicamentos"
            >
            <button type="submit" class="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-forest text-white" aria-label="Buscar">
              <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <circle cx="11" cy="11" r="6.5" />
                <path stroke-linecap="round" d="m16 16 4 4" />
              </svg>
            </button>
          </form>

          <div class="ml-auto flex items-center gap-1 sm:gap-2">
            <a href="#contacto" class="grid h-10 w-10 place-items-center rounded-full hover:bg-white/10" aria-label="Cuenta">
              <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
                <circle cx="12" cy="8" r="3.2" />
                <path stroke-linecap="round" d="M5 19.2c1.4-2.6 3.8-4 7-4s5.6 1.4 7 4" />
              </svg>
            </a>
            <a href="#productos" class="grid h-10 w-10 place-items-center rounded-full hover:bg-white/10" aria-label="Guardados">
              <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
                <path stroke-linejoin="round" d="M12 20s-7-4.4-7-9a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 4.6-7 9-7 9z" />
              </svg>
            </a>
            <a href="#productos" class="grid h-10 w-10 place-items-center rounded-full hover:bg-white/10" aria-label="Comparar precios">
              <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
                <path stroke-linejoin="round" d="M6 7h12l-1 12H7L6 7z" />
                <path stroke-linecap="round" d="M9 7a3 3 0 0 1 6 0" />
              </svg>
            </a>
            <button
              type="button"
              class="grid h-10 w-10 place-items-center rounded-full md:hidden"
              :aria-expanded="open"
              aria-controls="menu-movil"
              :aria-label="open ? 'Cerrar menú' : 'Abrir menú'"
              @click="open = !open"
            >
              <svg v-if="!open" viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path stroke-linecap="round" d="M4 7h16M4 12h16M4 17h16" />
              </svg>
              <svg v-else viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path stroke-linecap="round" d="M6 6l12 12M18 6 6 18" />
              </svg>
            </button>
          </div>
        </div>

        <div v-show="open" id="menu-movil" class="border-t border-white/10 px-4 pb-4 md:hidden">
          <form class="mt-3 flex items-center rounded-full bg-white p-1 text-ink" @submit.prevent="submitSearch">
            <input
              v-model="draft"
              type="search"
              placeholder="Busca medicamentos..."
              class="min-w-0 flex-1 bg-transparent px-3 py-2 text-sm outline-none"
              aria-label="Buscar medicamentos"
            >
            <button type="submit" class="grid h-9 w-9 place-items-center rounded-full bg-forest text-white" aria-label="Buscar">
              <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <circle cx="11" cy="11" r="6.5" />
                <path stroke-linecap="round" d="m16 16 4 4" />
              </svg>
            </button>
          </form>
          <label class="mt-3 block text-xs text-white/70">
            Entregar en
            <select v-model="city" class="mt-1 w-full rounded-xl bg-white px-3 py-2 text-sm text-ink">
              <option v-for="name in cities" :key="name">{{ name }}</option>
            </select>
          </label>
        </div>
      </div>
    </div>

    <div class="border-b border-[#E7E4DE] bg-cream">
      <div class="mx-auto flex items-center gap-1 px-4 sm:px-6" :class="anchoPagina">
        <nav class="no-scrollbar flex min-w-0 flex-1 items-center gap-1 overflow-x-auto py-2.5" aria-label="Categorías">
          <NuxtLink
            v-for="link in links"
            :key="link.label"
            :to="link.to"
            class="flex shrink-0 items-center gap-1.5 rounded-full px-3 py-2 text-sm text-ink hover:bg-white"
          >
            <svg v-if="link.icon" viewBox="0 0 24 24" class="h-4 w-4 text-forest" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
              <path stroke-linejoin="round" d="M4 6h6v6H4zM14 6h6v6h-6zM4 16h6v4H4zM14 16h6v4h-6z" />
            </svg>
            <span v-if="link.dot" class="h-1.5 w-1.5 rounded-full bg-sky-500" />
            {{ link.label }}
          </NuxtLink>
        </nav>
        <a href="#categorias" class="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-forest text-white" aria-label="Ver categorías">
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path stroke-linecap="round" d="M5 12h14M13 6l6 6-6 6" />
          </svg>
        </a>
      </div>
    </div>
  </header>
</template>
