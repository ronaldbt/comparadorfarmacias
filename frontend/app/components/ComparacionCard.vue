<script setup lang="ts">
import type { ProductoCatalogo } from '~/utils/catalogo'

const props = defineProps<{ producto: ProductoCatalogo }>()

const ofertas = computed(() => ofertasOrdenadas(props.producto.ofertas))
const ahorro = computed(() => ahorroEntreFarmacias(props.producto.ofertas))
const mejor = computed(() => ofertas.value[0]?.precio ?? null)

function esMejor(precio: number) {
  return precio === mejor.value
}
</script>

<template>
  <article class="flex h-full flex-col rounded-[1.6rem] border border-[#E7E4DE] bg-white p-4 shadow-card">
    <p class="text-[11px] font-semibold uppercase tracking-[0.16em] text-mute">
      {{ producto.marca || 'Medicamento' }}
    </p>
    <h3 class="mt-2 line-clamp-3 text-lg font-semibold leading-snug text-ink">
      {{ producto.nombre }}
    </h3>
    <p v-if="ahorro" class="mt-3 inline-flex w-fit rounded-full bg-forest-soft px-3 py-1 text-xs font-semibold text-forest">
      Ahorras {{ ahorro }}% entre farmacias
    </p>
    <ul class="mt-4 space-y-2">
      <li v-for="oferta in ofertas" :key="oferta.farmacia">
        <a
          v-if="oferta.url"
          :href="oferta.url"
          target="_blank"
          rel="noopener noreferrer"
          class="flex items-center justify-between gap-3 rounded-2xl px-3 py-2.5 text-sm"
          :class="esMejor(oferta.precio) ? 'bg-forest text-white' : 'bg-mist text-ink'"
        >
          <span class="min-w-0">
            <span class="block">{{ oferta.farmacia === 'Fonasa' ? 'Convenio Fonasa' : oferta.farmacia }}</span>
            <span v-if="oferta.detalle" class="block truncate text-xs opacity-80">{{ oferta.detalle }}</span>
          </span>
          <span class="shrink-0 font-semibold">{{ dinero(oferta.precio) }}</span>
        </a>
        <div
          v-else
          class="flex items-center justify-between gap-3 rounded-2xl px-3 py-2.5 text-sm"
          :class="esMejor(oferta.precio) ? 'bg-forest text-white' : 'bg-mist text-ink'"
        >
          <span class="min-w-0">
            <span class="block">{{ oferta.farmacia === 'Fonasa' ? 'Convenio Fonasa' : oferta.farmacia }}</span>
            <span v-if="oferta.detalle" class="block truncate text-xs opacity-80">{{ oferta.detalle }}</span>
          </span>
          <span class="shrink-0 font-semibold">{{ dinero(oferta.precio) }}</span>
        </div>
      </li>
    </ul>
  </article>
</template>
