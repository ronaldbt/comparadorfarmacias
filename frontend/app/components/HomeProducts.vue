<script setup lang="ts">
type Offer = {
  pharmacy: string
  price: number
  eta: string
}

type Product = {
  id: string
  name: string
  detail: string
  reviews: number
  badge?: string
  topic: 'alergia' | 'solar' | 'hidratacion'
  variant: 'sand' | 'blue' | 'mint' | 'lilac'
  offers: Offer[]
}

const products: Product[] = [
  {
    id: 'paracetamol',
    name: 'Paracetamol 500 mg',
    detail: 'Caja 16 comprimidos',
    reviews: 214,
    badge: 'Top',
    topic: 'alergia',
    variant: 'sand',
    offers: [
      { pharmacy: 'Farmacia Alba', price: 1990, eta: 'Retiro hoy' },
      { pharmacy: 'Botica Norte', price: 2290, eta: 'Despacho mañana' },
      { pharmacy: 'Farmacia Sol', price: 2490, eta: 'Retiro en 2 h' }
    ]
  },
  {
    id: 'ibuprofeno',
    name: 'Ibuprofeno 400 mg',
    detail: 'Caja 20 comprimidos',
    reviews: 168,
    topic: 'alergia',
    variant: 'blue',
    offers: [
      { pharmacy: 'Botica Norte', price: 3290, eta: 'Retiro hoy' },
      { pharmacy: 'Verde Express', price: 3590, eta: 'Despacho hoy' },
      { pharmacy: 'Farmacia Alba', price: 3890, eta: 'Retiro mañana' }
    ]
  },
  {
    id: 'omeprazol',
    name: 'Omeprazol 20 mg',
    detail: 'Caja 14 cápsulas',
    reviews: 96,
    badge: '−15%',
    topic: 'hidratacion',
    variant: 'mint',
    offers: [
      { pharmacy: 'Farmacia Sol', price: 4150, eta: 'Retiro hoy' },
      { pharmacy: 'Farmacia Alba', price: 4490, eta: 'Despacho mañana' },
      { pharmacy: 'Botica Norte', price: 4790, eta: 'Retiro en 2 h' }
    ]
  },
  {
    id: 'vitamina',
    name: 'Vitamina D3 1000 UI',
    detail: 'Frasco 60 cápsulas',
    reviews: 73,
    topic: 'solar',
    variant: 'lilac',
    offers: [
      { pharmacy: 'Verde Express', price: 6490, eta: 'Despacho hoy' },
      { pharmacy: 'Farmacia Sol', price: 6990, eta: 'Retiro hoy' },
      { pharmacy: 'Botica Norte', price: 7290, eta: 'Retiro mañana' }
    ]
  },
  {
    id: 'cetirizina',
    name: 'Cetirizina 10 mg',
    detail: 'Caja 10 comprimidos',
    reviews: 141,
    badge: 'Nuevo',
    topic: 'alergia',
    variant: 'mint',
    offers: [
      { pharmacy: 'Farmacia Alba', price: 2890, eta: 'Retiro hoy' },
      { pharmacy: 'Farmacia Sol', price: 3190, eta: 'Despacho mañana' },
      { pharmacy: 'Verde Express', price: 3390, eta: 'Retiro en 2 h' }
    ]
  },
  {
    id: 'spray',
    name: 'Spray nasal',
    detail: 'Frasco 10 ml',
    reviews: 88,
    topic: 'alergia',
    variant: 'blue',
    offers: [
      { pharmacy: 'Botica Norte', price: 4590, eta: 'Retiro hoy' },
      { pharmacy: 'Farmacia Alba', price: 4890, eta: 'Despacho hoy' },
      { pharmacy: 'Farmacia Sol', price: 5120, eta: 'Retiro mañana' }
    ]
  },
  {
    id: 'protector',
    name: 'Protector solar SPF 50',
    detail: 'Envase 50 ml',
    reviews: 203,
    badge: 'Nuevo',
    topic: 'solar',
    variant: 'sand',
    offers: [
      { pharmacy: 'Verde Express', price: 7990, eta: 'Despacho hoy' },
      { pharmacy: 'Farmacia Sol', price: 8490, eta: 'Retiro hoy' },
      { pharmacy: 'Botica Norte', price: 8990, eta: 'Retiro mañana' }
    ]
  },
  {
    id: 'suero',
    name: 'Suero de rehidratación',
    detail: 'Caja 4 sobres',
    reviews: 64,
    topic: 'hidratacion',
    variant: 'lilac',
    offers: [
      { pharmacy: 'Farmacia Alba', price: 2490, eta: 'Retiro hoy' },
      { pharmacy: 'Botica Norte', price: 2790, eta: 'Despacho mañana' },
      { pharmacy: 'Farmacia Sol', price: 2990, eta: 'Retiro en 2 h' }
    ]
  }
]

const { query, topic } = useCatalog()

const tabs = [
  { id: 'alergia' as const, label: 'Alergias', count: 14 },
  { id: 'solar' as const, label: 'Protección solar', count: 9 },
  { id: 'hidratacion' as const, label: 'Hidratación', count: 11 }
]

const visibleProducts = computed(() => {
  const text = query.value.trim().toLowerCase()
  return products.filter((product) => {
    const matchesTopic = text ? true : product.topic === topic.value
    const haystack = `${product.name} ${product.detail}`.toLowerCase()
    return matchesTopic && (!text || haystack.includes(text))
  })
})

function stepTopic(direction: number) {
  const index = tabs.findIndex(tab => tab.id === topic.value)
  const next = (index + direction + tabs.length) % tabs.length
  const tab = tabs[next]
  if (tab) topic.value = tab.id
}

const saved = ref<Record<string, boolean>>({})
const active = ref<Product | null>(null)
const dialog = ref<HTMLDialogElement | null>(null)

const sortedOffers = computed(() => {
  if (!active.value) return []
  return [...active.value.offers].sort((a, b) => a.price - b.price)
})

const lowestPrice = (product: Product) => Math.min(...product.offers.map(offer => offer.price))

function money(value: number) {
  return `$${value.toLocaleString('es-CL')}`
}

async function openCompare(product: Product) {
  active.value = product
  await nextTick()
  dialog.value?.showModal()
}

function closeCompare() {
  dialog.value?.close()
}

function onBackdrop(event: MouseEvent) {
  if (event.target === dialog.value) closeCompare()
}
</script>

<template>
  <section class="scroll-mt-36">
    <div id="productos" class="scroll-mt-36 mx-auto max-w-6xl px-4 pb-8 pt-4 sm:px-6">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h2 class="text-2xl font-semibold tracking-tight text-forest sm:text-3xl">Destacados este mes</h2>
        <div class="flex items-center gap-1 sm:gap-2">
          <div class="no-scrollbar flex gap-1 overflow-x-auto">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              type="button"
              class="shrink-0 rounded-full px-3 py-1.5 text-sm"
              :class="topic === tab.id && !query ? 'font-semibold text-forest' : 'text-mute'"
              @click="topic = tab.id; query = ''"
            >
              {{ tab.label }} ({{ tab.count }})
            </button>
          </div>
          <button type="button" class="grid h-9 w-9 shrink-0 place-items-center rounded-full border border-[#E4E0D8] text-forest" aria-label="Grupo anterior" @click="stepTopic(-1)">
            <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path stroke-linecap="round" d="M19 12H5M11 6l-6 6 6 6" />
            </svg>
          </button>
          <button type="button" class="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-forest text-white" aria-label="Grupo siguiente" @click="stepTopic(1)">
            <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path stroke-linecap="round" d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
        </div>
      </div>

      <p v-if="query" class="mt-4 text-sm text-mute">
        Resultados para «{{ query }}».
        <button type="button" class="font-medium text-forest underline" @click="query = ''">Ver destacados</button>
      </p>
      <p v-if="visibleProducts.length === 0" class="mt-8 text-sm text-mute">No encontramos ese producto. Prueba con otro nombre.</p>

      <ul class="mt-6 grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
        <li
          v-for="product in visibleProducts"
          :key="product.id"
          class="flex flex-col rounded-[1.4rem] bg-white p-3 shadow-card ring-1 ring-[#ECEAE4]"
        >
          <div class="relative overflow-hidden rounded-[1.1rem]">
            <ProductArt :variant="product.variant" class="block h-48 w-full sm:h-52" />
            <span
              v-if="product.badge"
              class="absolute left-3 top-3 rounded-full bg-white/95 px-2.5 py-1 text-[11px] font-semibold text-forest"
            >
              {{ product.badge }}
            </span>
            <button
              type="button"
              class="absolute right-3 top-3 grid h-8 w-8 place-items-center rounded-full bg-white/95 text-forest shadow-sm"
              :aria-pressed="Boolean(saved[product.id])"
              :aria-label="saved[product.id] ? `Quitar ${product.name} de guardados` : `Guardar ${product.name}`"
              @click="saved[product.id] = !saved[product.id]"
            >
              <svg viewBox="0 0 24 24" class="h-4 w-4" :fill="saved[product.id] ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path stroke-linejoin="round" d="M12 20s-7-4.4-7-9a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 4.6-7 9-7 9z" />
              </svg>
            </button>
          </div>

          <div class="flex flex-1 flex-col px-2 pb-2 pt-4">
            <p class="text-xs text-mute">
              Desde <span class="font-medium text-ink">{{ money(lowestPrice(product)) }}</span>
            </p>
            <h3 class="mt-1 text-[15px] font-semibold leading-snug text-forest">{{ product.name }}</h3>
            <p class="mt-0.5 text-xs text-mute">{{ product.detail }}</p>
            <div class="mt-2 flex items-center gap-1" :aria-label="`Valoración de ${product.reviews} reseñas`">
              <svg v-for="star in 5" :key="star" viewBox="0 0 20 20" class="h-3.5 w-3.5 text-gold" fill="currentColor" aria-hidden="true">
                <path d="M10 1.8 12.4 7l5.6.5-4.3 3.6 1.3 5.4L10 13.8 4.9 16.5l1.3-5.4L2 7.5 7.6 7 10 1.8z" />
              </svg>
              <span class="ml-1 text-xs text-mute">({{ product.reviews }})</span>
            </div>
            <button
              type="button"
              class="mt-4 w-fit rounded-full bg-forest px-4 py-1.5 text-xs font-medium text-white transition-colors hover:bg-forest-deep"
              @click="openCompare(product)"
            >
              Ver precio
            </button>
          </div>
        </li>
      </ul>
    </div>

    <dialog ref="dialog" class="w-full max-w-md" aria-labelledby="comparar-titulo" @click="onBackdrop">
      <div v-if="active" class="rounded-[1.6rem] bg-white p-6 shadow-card ring-1 ring-[#ECEAE4]" @click.stop>
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-xs font-medium uppercase tracking-[0.14em] text-mute">Precios de hoy</p>
            <h2 id="comparar-titulo" class="mt-1 font-serif text-2xl text-forest">{{ active.name }}</h2>
            <p class="mt-1 text-sm text-mute">{{ active.detail }} · precios referenciales</p>
          </div>
          <button
            type="button"
            class="grid h-9 w-9 shrink-0 place-items-center rounded-full text-forest hover:bg-mist"
            aria-label="Cerrar comparación"
            @click="closeCompare"
          >
            <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path stroke-linecap="round" d="M6 6l12 12M18 6 6 18" />
            </svg>
          </button>
        </div>

        <ul class="mt-5 space-y-2">
          <li
            v-for="(offer, index) in sortedOffers"
            :key="offer.pharmacy"
            class="flex items-center justify-between gap-3 rounded-2xl px-4 py-3"
            :class="index === 0 ? 'bg-forest-soft' : 'bg-mist'"
          >
            <div>
              <p class="text-sm font-medium text-forest">{{ offer.pharmacy }}</p>
              <p class="text-xs text-mute">{{ offer.eta }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold text-forest">{{ money(offer.price) }}</p>
              <p v-if="index === 0" class="text-[11px] font-medium text-[#1F6B5A]">Mejor precio</p>
            </div>
          </li>
        </ul>
      </div>
    </dialog>
  </section>
</template>
