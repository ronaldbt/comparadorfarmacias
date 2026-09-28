<script setup lang="ts">
type Medicamento = {
  clave: string
  nombre: string
  principio: string | null
  presentacion: string
  accion: string | null
  laboratorio: string | null
  equivalencia: string | null
  registro: string | null
  ofertaFonasa: number | null
}

type PrecioSimi = {
  nombre: string
  marca: string | null
  principio: string | null
  bioequivalente: boolean
  precio: number | null
  precioLista: number | null
  disponible: boolean
  registro: string | null
  url: string | null
}

type Sucursal = {
  farmacia: string
  sucursal: string
  direccion: string
  comuna: string
  distancia: number | null
  precioNormal: number | null
  ofertaFonasa: number | null
  ahorro: number | null
  ahorroAnual: number | null
  horario: string
}

type Respuesta = {
  consulta: string
  tipo: 'nombre' | 'principio'
  fonasa: Medicamento[]
  simi: PrecioSimi[]
  avisos: string[]
}

const lugares = [
  { id: 'santiago', label: 'Santiago centro', lat: -33.4489, lng: -70.6693 },
  { id: 'providencia', label: 'Providencia', lat: -33.4264, lng: -70.6168 },
  { id: 'las-condes', label: 'Las Condes', lat: -33.4086, lng: -70.5696 },
  { id: 'maipu', label: 'Maipú', lat: -33.511, lng: -70.757 },
  { id: 'valparaiso', label: 'Valparaíso', lat: -33.0472, lng: -71.6127 },
  { id: 'concepcion', label: 'Concepción', lat: -36.827, lng: -73.0503 }
]

const route = useRoute()
const termino = ref(typeof route.query.q === 'string' ? route.query.q : '')
const tipo = ref(route.query.tipo === 'principio' ? 'principio' : 'nombre')
const lugar = ref('santiago')
const abierto = ref<string | null>(null)
const sucursales = ref<Sucursal[]>([])
const cargandoSucursales = ref(false)
const errorSucursales = ref('')

const consulta = computed(() => typeof route.query.q === 'string' ? route.query.q : '')
const tipoRuta = computed(() => route.query.tipo === 'principio' ? 'principio' : 'nombre')
const punto = computed(() => lugares.find(item => item.id === lugar.value) ?? lugares[0])

watch(() => route.query.q, (value) => {
  termino.value = typeof value === 'string' ? value : ''
})

watch(() => route.query.tipo, (value) => {
  tipo.value = value === 'principio' ? 'principio' : 'nombre'
})

const { data, pending, error } = await useAsyncData(
  'comparar',
  () => {
    if (consulta.value.trim().length < 2) return Promise.resolve(null)
    return $fetch<Respuesta>('/api/comparar', {
      query: {
        q: consulta.value,
        tipo: tipoRuta.value,
        lat: punto.value.lat,
        lng: punto.value.lng
      }
    })
  },
  { watch: [consulta, tipoRuta, lugar] }
)

useSeoMeta({
  title: () => consulta.value ? `${consulta.value} — precios Salvia` : 'Comparar precios — Salvia',
  description: 'Precio de convenio Fonasa y precio público de Dr. Simi para el mismo medicamento.'
})

const clp = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 })

function dinero(value: number | null) {
  return value == null ? '—' : clp.format(value)
}

function distancia(metros: number | null) {
  if (metros == null) return ''
  if (metros < 1000) return `${metros} m`
  return `${(metros / 1000).toFixed(1)} km`
}

function etiquetaEquivalencia(value: string | null) {
  const texto = (value || '').toUpperCase()
  if (texto.includes('BIO')) return 'Bioequivalente'
  if (texto.includes('GENER')) return 'Genérico'
  if (texto.includes('EQUIVALENTE')) return 'Equivalente terapéutico'
  if (!texto || texto.includes('NO REGISTRA')) return 'Sin bioequivalencia registrada'
  return value
}

function buscar() {
  const q = termino.value.trim()
  if (q.length < 2) return
  abierto.value = null
  navigateTo({ path: '/comparar', query: { q, tipo: tipo.value } })
}

async function verSucursales(medicamento: Medicamento) {
  if (abierto.value === medicamento.clave) {
    abierto.value = null
    return
  }
  abierto.value = medicamento.clave
  sucursales.value = []
  errorSucursales.value = ''
  cargandoSucursales.value = true
  try {
    const respuesta = await $fetch<{ farmacias: Sucursal[] }>('/api/comparar/farmacias', {
      method: 'POST',
      body: {
        lat: punto.value.lat,
        lng: punto.value.lng,
        nombre: medicamento.nombre,
        registro: medicamento.registro,
        presentacion: medicamento.presentacion,
        laboratorio: medicamento.laboratorio
      }
    })
    sucursales.value = respuesta.farmacias
  } catch {
    errorSucursales.value = 'No pude cargar las sucursales de este medicamento.'
  } finally {
    cargandoSucursales.value = false
  }
}
</script>

<template>
  <main class="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10">
    <p class="text-sm font-medium text-forest">Comparador</p>
    <h1 class="mt-1 font-serif text-3xl text-ink sm:text-4xl">Precios reales de medicamentos</h1>
    <p class="mt-3 max-w-2xl text-sm leading-6 text-mute">
      El convenio Fonasa muestra el precio a pagar en farmacias adheridas cerca de la comuna que elijas.
      Dr. Simi muestra el precio público de su tienda. Ahumada y Cruz Verde todavía no entran: no publican una API de precios.
    </p>

    <form class="mt-6 rounded-3xl bg-white p-4 shadow-card sm:p-5" @submit.prevent="buscar">
      <div class="flex flex-col gap-3 sm:flex-row">
        <div class="flex rounded-full bg-mist p-1 text-sm">
          <button
            type="button"
            class="rounded-full px-4 py-2"
            :class="tipo === 'nombre' ? 'bg-forest text-white' : 'text-ink'"
            @click="tipo = 'nombre'"
          >
            Nombre
          </button>
          <button
            type="button"
            class="rounded-full px-4 py-2"
            :class="tipo === 'principio' ? 'bg-forest text-white' : 'text-ink'"
            @click="tipo = 'principio'"
          >
            Principio activo
          </button>
        </div>
        <input
          v-model="termino"
          type="search"
          placeholder="Paracetamol, losartán, ibuprofeno..."
          class="min-w-0 flex-1 rounded-full border border-[#E7E4DE] px-4 py-3 text-sm outline-none focus:border-forest"
          aria-label="Medicamento"
        >
        <button type="submit" class="rounded-full bg-[#F5C518] px-5 py-3 text-sm font-semibold text-ink">
          Buscar
        </button>
      </div>
      <div class="mt-4 flex gap-2 overflow-x-auto no-scrollbar" aria-label="Comuna de referencia">
        <button
          v-for="item in lugares"
          :key="item.id"
          type="button"
          class="shrink-0 rounded-full px-3 py-1.5 text-sm"
          :class="lugar === item.id ? 'bg-forest text-white' : 'bg-mist text-ink'"
          @click="lugar = item.id"
        >
          {{ item.label }}
        </button>
      </div>
    </form>

    <p v-if="consulta.trim().length < 2" class="mt-8 text-sm text-mute">Busca un medicamento para ver precios.</p>
    <p v-else-if="pending" class="mt-8 text-sm text-mute">Buscando {{ consulta }}…</p>
    <p v-else-if="error" class="mt-8 text-sm text-ink">No se pudo completar la búsqueda. Prueba con otro nombre.</p>

    <template v-else-if="data">
      <p v-for="aviso in data.avisos" :key="aviso" class="mt-6 rounded-2xl bg-sand px-4 py-3 text-sm text-ink">
        {{ aviso }}
      </p>

      <section class="mt-8">
        <h2 class="font-serif text-2xl text-ink">Convenio Fonasa</h2>
        <p class="mt-1 text-sm text-mute">
          Precio referencial del convenio cerca de {{ punto.label }}. En caja hay que mostrar el RUT y, si corresponde, la receta.
        </p>
        <p v-if="data.fonasa.length === 0" class="mt-4 text-sm text-mute">Fonasa no devolvió presentaciones para esta búsqueda.</p>
        <ul v-else class="mt-4 grid gap-3">
          <li v-for="med in data.fonasa" :key="med.clave" class="rounded-3xl bg-white p-4 shadow-card sm:p-5">
            <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div class="min-w-0">
                <p class="text-xs font-medium uppercase tracking-wide text-forest">{{ etiquetaEquivalencia(med.equivalencia) }}</p>
                <h3 class="mt-1 text-lg font-semibold text-ink">{{ med.nombre }}</h3>
                <p class="text-sm text-ink">{{ med.presentacion }}</p>
                <p class="mt-1 text-sm text-mute">{{ med.principio }} · {{ med.laboratorio }}</p>
                <p v-if="med.accion" class="text-sm text-mute">{{ med.accion }}</p>
              </div>
              <div class="sm:text-right">
                <p class="text-xs text-mute">Oferta Fonasa</p>
                <p class="font-serif text-2xl text-ink">{{ dinero(med.ofertaFonasa) }}</p>
                <button
                  type="button"
                  class="mt-2 rounded-full bg-forest px-4 py-2 text-sm text-white"
                  @click="verSucursales(med)"
                >
                  {{ abierto === med.clave ? 'Ocultar sucursales' : 'Ver sucursales cercanas' }}
                </button>
              </div>
            </div>
            <div v-if="abierto === med.clave" class="mt-4 border-t border-[#E7E4DE] pt-4">
              <p v-if="cargandoSucursales" class="text-sm text-mute">Buscando locales…</p>
              <p v-else-if="errorSucursales" class="text-sm text-ink">{{ errorSucursales }}</p>
              <p v-else-if="sucursales.length === 0" class="text-sm text-mute">No hay sucursales adheridas cerca de este punto.</p>
              <ul v-else class="grid gap-2">
                <li v-for="local in sucursales" :key="`${local.farmacia}-${local.sucursal}-${local.direccion}`" class="rounded-2xl bg-mist px-4 py-3 text-sm">
                  <div class="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
                    <p class="font-semibold text-ink">{{ local.farmacia }} · {{ local.sucursal }}</p>
                    <p class="text-mute">{{ distancia(local.distancia) }}</p>
                  </div>
                  <p class="text-mute">{{ local.direccion }}<span v-if="local.comuna">, {{ local.comuna }}</span></p>
                  <p class="mt-1 text-ink">
                    Lista {{ dinero(local.precioNormal) }} · Fonasa {{ dinero(local.ofertaFonasa) }}
                    <span v-if="local.ahorro"> · ahorras {{ dinero(local.ahorro) }} en esta compra, {{ dinero(local.ahorroAnual) }} si se repite cada mes</span>
                  </p>
                  <p v-if="local.horario" class="text-mute">{{ local.horario }}</p>
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </section>

      <section class="mt-10">
        <h2 class="font-serif text-2xl text-ink">Dr. Simi, precio público</h2>
        <p class="mt-1 text-sm text-mute">Precio publicado en su tienda. No es el precio de convenio ni el de otra cadena.</p>
        <p v-if="data.simi.length === 0" class="mt-4 text-sm text-mute">Dr. Simi no publicó productos para esta búsqueda.</p>
        <ul v-else class="mt-4 grid gap-3 sm:grid-cols-2">
          <li v-for="item in data.simi" :key="item.url || item.nombre" class="rounded-3xl bg-white p-4 shadow-card">
            <p class="text-xs font-medium uppercase tracking-wide text-forest">
              {{ item.bioequivalente ? 'Bioequivalente' : 'Sin sello de bioequivalente' }}
            </p>
            <h3 class="mt-1 text-lg font-semibold text-ink">{{ item.nombre }}</h3>
            <p class="text-sm text-mute">{{ item.marca }}<span v-if="item.principio"> · {{ item.principio }}</span></p>
            <p class="mt-2 font-serif text-2xl text-ink">{{ dinero(item.precio) }}</p>
            <p class="text-sm text-mute">{{ item.disponible ? 'Disponible en la tienda' : 'Sin stock publicado' }}</p>
            <a
              v-if="item.url"
              :href="item.url"
              target="_blank"
              rel="noopener noreferrer"
              class="mt-3 inline-flex rounded-full bg-forest-soft px-4 py-2 text-sm font-medium text-forest"
            >
              Ver en Dr. Simi
            </a>
          </li>
        </ul>
      </section>

      <p class="mt-10 max-w-3xl text-xs leading-5 text-mute">
        Los montos de Fonasa salen del buscador oficial de medicamentos en convenio y pueden cambiar según la sucursal.
        El ahorro anual es el ahorro del convenio multiplicado por 12, como referencia de un tratamiento mensual.
        El precio de Dr. Simi es el de su catálogo público al momento de la búsqueda.
      </p>
    </template>
  </main>
</template>
