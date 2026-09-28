<script setup lang="ts">
import type { ProductoCatalogo } from '~/utils/catalogo'
const busqueda = ref('')
const farmacias = [
  'Ahumada', 'Salcobrand', 'Knop', 'Dr. Simi', 'La Botika', 'Farmex',
  'EcoFarmacias', 'EasyFarma', 'Novasalud', 'Farmazon', 'Fonasa',
]
const activas = ref<string[]>([...farmacias])
const soloAhorro = ref(false)
const orden = ref<'ahorro' | 'precio'>('ahorro')
const pagina = ref(1)
const porPagina = 24

function recortar(producto: ProductoCatalogo): ProductoCatalogo {
  return {
    ...producto,
    ofertas: producto.ofertas.filter(oferta => activas.value.includes(oferta.farmacia))
  }
}

const visibles = computed(() => {
  const texto = busqueda.value.trim().toLowerCase()
  const lista = productosCatalogo.flatMap((producto) => {
    const coincide = !texto || `${producto.nombre} ${producto.marca || ''} ${producto.consulta}`.toLowerCase().includes(texto)
    if (!coincide) return []
    const visible = recortar(producto)
    if (visible.ofertas.length === 0) return []
    if (soloAhorro.value && ahorroEntreFarmacias(visible.ofertas) == null) return []
    return [visible]
  })
  return lista.sort((a, b) => {
    if (orden.value === 'precio') return menorPrecio(a.ofertas) - menorPrecio(b.ofertas)
    return (ahorroEntreFarmacias(b.ofertas) || 0) - (ahorroEntreFarmacias(a.ofertas) || 0)
  })
})

const paginas = computed(() => Math.max(1, Math.ceil(visibles.value.length / porPagina)))
const enPagina = computed(() => {
  const inicio = (pagina.value - 1) * porPagina
  return visibles.value.slice(inicio, inicio + porPagina)
})

watch([busqueda, activas, soloAhorro, orden], () => {
  pagina.value = 1
})

function alternar(farmacia: string) {
  activas.value = activas.value.includes(farmacia)
    ? activas.value.filter(item => item !== farmacia)
    : [...activas.value, farmacia]
}

useSeoMeta({
  title: 'Remedios — Salvia',
  description: 'Listado de medicamentos con el precio publicado por cada farmacia que lo vende, y el convenio Fonasa.'
})
</script>

<template>
  <main class="mx-auto grid max-w-[1480px] gap-8 px-4 py-8 sm:px-6 lg:grid-cols-[240px_minmax(0,1fr)] lg:py-10">
    <aside class="h-fit rounded-[1.6rem] border border-[#E7E4DE] bg-white p-5 lg:sticky lg:top-28">
      <h1 class="font-serif text-2xl text-ink">Filtros</h1>
      <label class="mt-4 block text-sm text-mute">
        Medicamento
        <input
          v-model="busqueda"
          type="search"
          placeholder="Paracetamol, losartán..."
          class="mt-1 w-full rounded-2xl border border-[#E7E4DE] px-3 py-2 text-sm text-ink outline-none focus:border-forest"
        >
      </label>
      <fieldset class="mt-5">
        <legend class="text-sm font-medium text-ink">Farmacia</legend>
        <p class="mt-1 text-xs leading-5 text-mute">
          Cada casilla esconde o muestra el precio de esa farmacia. Si un remedio no tiene precio publicado ahí, esa fila no aparece.
        </p>
        <label v-for="farmacia in farmacias" :key="farmacia" class="mt-2 flex items-center gap-2 text-sm text-ink">
          <input
            type="checkbox"
            class="accent-[#0A3D36]"
            :checked="activas.includes(farmacia)"
            @change="alternar(farmacia)"
          >
          {{ farmacia === 'Fonasa' ? 'Convenio Fonasa' : farmacia }}
        </label>
      </fieldset>
      <label class="mt-5 flex items-start gap-2 text-sm text-ink">
        <input v-model="soloAhorro" type="checkbox" class="mt-0.5 accent-[#0A3D36]">
        Solo si las farmacias marcadas tienen precios distintos
      </label>
      <label class="mt-5 block text-sm text-mute">
        Orden
        <select v-model="orden" class="mt-1 w-full rounded-2xl border border-[#E7E4DE] bg-white px-3 py-2 text-sm text-ink">
          <option value="ahorro">Mayor ahorro</option>
          <option value="precio">Menor precio</option>
        </select>
      </label>
    </aside>

    <section>
      <p class="text-sm font-medium text-forest">Catálogo</p>
      <h2 class="mt-1 font-serif text-3xl text-ink">Todos los remedios con precio</h2>
      <p class="mt-2 text-sm text-mute">{{ visibles.length }} medicamentos con los precios marcados.</p>
      <p v-if="activas.length === 0" class="mt-8 text-sm text-mute">Marca al menos una farmacia para ver precios.</p>
      <p v-else-if="visibles.length === 0" class="mt-8 text-sm text-mute">Ningún remedio coincide con esos filtros.</p>
      <ul v-else class="mt-6 grid max-w-[1040px] gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <li v-for="producto in enPagina" :key="producto.id">
          <ComparacionCard :producto="producto" />
        </li>
      </ul>
      <div v-if="paginas > 1" class="mt-8 flex items-center justify-between gap-3 text-sm">
        <button type="button" class="rounded-full bg-mist px-4 py-2 text-ink disabled:opacity-40" :disabled="pagina <= 1" @click="pagina -= 1">
          Anterior
        </button>
        <p class="text-mute">Página {{ pagina }} de {{ paginas }}</p>
        <button type="button" class="rounded-full bg-mist px-4 py-2 text-ink disabled:opacity-40" :disabled="pagina >= paginas" @click="pagina += 1">
          Siguiente
        </button>
      </div>
    </section>
  </main>
</template>
