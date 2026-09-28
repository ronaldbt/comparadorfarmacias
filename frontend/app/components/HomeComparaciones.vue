<script setup lang="ts">
const destacados = productosCatalogo.filter(producto => producto.destacado).slice(0, 8)
</script>

<template>
  <section id="productos" class="scroll-mt-28 px-4 py-12 sm:px-6">
    <div class="mx-auto max-w-6xl">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p class="text-sm font-medium text-forest">Precios de hoy</p>
          <h2 class="mt-1 font-serif text-3xl text-ink sm:text-4xl">Los 8 medicamentos que más se comparan</h2>
        </div>
        <p class="max-w-sm text-sm leading-6 text-mute">
          El precio más bajo va marcado. El porcentaje compara las farmacias que publican precio de góndola. Fonasa es el convenio.
        </p>
      </div>

      <p v-if="destacados.length === 0" class="mt-8 text-sm text-mute">
        Todavía no hay un barrido de precios guardado.
      </p>
      <ul v-else class="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <li v-for="producto in destacados" :key="producto.id">
          <ComparacionCard :producto="producto" />
        </li>
      </ul>

      <div class="mt-8">
        <NuxtLink to="/remedios" class="inline-flex items-center gap-2 rounded-full bg-forest px-5 py-2.5 text-sm font-semibold text-white">
          Ver más
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path stroke-linecap="round" d="M5 12h14M13 6l6 6-6 6" />
          </svg>
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
