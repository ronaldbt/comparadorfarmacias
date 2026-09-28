<script setup lang="ts">
const steps = [
  {
    title: 'Escribe el medicamento',
    text: 'Busca por nombre, principio activo o receta. En segundos ves las presentaciones que sí se venden.',
    image: '/images/consulta.jpg',
    alt: 'Médica con bata blanca y una carpeta de recetas'
  },
  {
    title: 'Compara farmacias',
    text: 'El mismo producto, varios precios. Ordenamos por cercanía, despacho y el valor más bajo.',
    image: '/images/farmacia.jpg',
    alt: 'Farmacéutica tomando un medicamento de la estantería'
  },
  {
    title: 'Compra donde te conviene',
    text: 'Te llevamos a la farmacia elegida para retirar o pedir despacho, sin cuentas de más.',
    image: '/images/entrega.jpg',
    alt: 'Persona eligiendo un producto en el pasillo de una farmacia'
  }
]
</script>

<template>
  <section id="simple" class="scroll-mt-24 px-4 py-16 sm:px-6 md:py-24">
    <div class="mx-auto max-w-5xl">
      <h2 class="text-center font-serif text-3xl tracking-tight text-forest sm:text-4xl">
        Hicimos el cuidado de la salud más simple
      </h2>

      <ul class="mt-12 grid gap-5 md:grid-cols-3">
        <li
          v-for="step in steps"
          :key="step.title"
          class="rounded-[1.4rem] bg-white p-3 shadow-card ring-1 ring-[#ECEAE4]"
        >
          <img
            :src="step.image"
            :alt="step.alt"
            width="640"
            height="480"
            class="aspect-[4/3] w-full rounded-xl object-cover"
            loading="lazy"
          >
          <div class="px-2 pb-3 pt-4">
            <h3 class="text-[15px] font-semibold text-forest">{{ step.title }}</h3>
            <p class="mt-2 text-sm leading-relaxed text-mute">{{ step.text }}</p>
          </div>
        </li>
      </ul>
    </div>
  </section>
</template>
