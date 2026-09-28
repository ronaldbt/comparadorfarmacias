<script setup lang="ts">
const reviews = [
  [
    {
      quote: 'Encontré el mismo omeprazol bastante más barato a tres cuadras. Dejé de recorrer locales.',
      name: 'Camila R.',
      place: 'Madrid',
      avatar: '/images/avatar-1.jpg'
    },
    {
      quote: 'Comparé la receta de mi madre en un minuto. El precio y el despacho quedaron claros antes de salir.',
      name: 'Mateo L.',
      place: 'Bogotá',
      avatar: '/images/avatar-2.jpg'
    },
    {
      quote: 'Uso Salvia cada mes para el tratamiento. Siempre aparece primero la farmacia que me conviene.',
      name: 'Carmen V.',
      place: 'Ciudad de México',
      avatar: '/images/avatar-3.jpg'
    }
  ],
  [
    {
      quote: 'Pasé de cinco pestañas a una sola lista. El ahorro se nota cuando el tratamiento es crónico.',
      name: 'Andrés P.',
      place: 'Buenos Aires',
      avatar: '/images/avatar-4.jpg'
    },
    {
      quote: 'Me avisó que había una presentación más económica con el mismo principio activo.',
      name: 'Lucía M.',
      place: 'Lima',
      avatar: '/images/avatar-5.jpg'
    },
    {
      quote: 'Retiré en la farmacia de la esquina y pagué menos que en la cadena de siempre.',
      name: 'Diego S.',
      place: 'Quito',
      avatar: '/images/avatar-6.jpg'
    }
  ]
]

const page = ref(0)
const visible = computed(() => reviews[page.value] ?? reviews[0])

const benefits = [
  {
    title: 'Mejor precio',
    text: 'El valor más bajo queda marcado para que no lo pases por alto.',
    icon: 'tag'
  },
  {
    title: 'Entrega rápida',
    text: 'Ves qué farmacias despachan hoy y cuáles tienen retiro inmediato.',
    icon: 'truck'
  },
  {
    title: 'Pago seguro',
    text: 'Pagas directo en la farmacia, con los medios que ya usa el local.',
    icon: 'shield'
  }
]
</script>

<template>
  <section class="px-4 py-16 sm:px-6 md:py-24" aria-labelledby="confianza-titulo">
    <div class="mx-auto max-w-5xl">
      <div class="flex justify-center gap-1 text-gold" aria-hidden="true">
        <svg v-for="star in 5" :key="star" viewBox="0 0 20 20" class="h-5 w-5" fill="currentColor">
          <path d="M10 1.8 12.4 7l5.6.5-4.3 3.6 1.3 5.4L10 13.8 4.9 16.5l1.3-5.4L2 7.5 7.6 7 10 1.8z" />
        </svg>
      </div>
      <h2 id="confianza-titulo" class="mt-3 text-center font-serif text-3xl tracking-tight text-forest sm:text-4xl">
        La confianza de más de 50.000 familias
      </h2>

      <ul class="mt-12 grid gap-4 md:grid-cols-3">
        <li
          v-for="(review, index) in visible"
          :key="review.name"
          class="flex flex-col rounded-[1.4rem] p-6"
          :class="index === 1 ? 'bg-blush' : 'bg-mist'"
        >
          <span class="grid h-8 w-8 place-items-center rounded-lg bg-forest text-white" aria-hidden="true">
            <svg viewBox="0 0 24 24" class="h-3.5 w-3.5" fill="currentColor">
              <path d="M7.1 6C4.7 7.6 3.3 10 3.3 13.1V18h6.1v-6.1H6.5c.1-1.8.8-3.2 2.3-4.2L7.1 6zm9.5 0c-2.4 1.6-3.8 4-3.8 7.1V18H18.9v-6.1h-2.9c.1-1.8.8-3.2 2.3-4.2L16.6 6z" />
            </svg>
          </span>
          <p class="mt-4 flex-1 text-sm leading-relaxed text-ink/85">“{{ review.quote }}”</p>
          <div class="mt-6 flex items-center gap-3">
            <img
              :src="review.avatar"
              :alt="''"
              width="40"
              height="40"
              class="h-10 w-10 rounded-full object-cover"
              loading="lazy"
            >
            <div>
              <p class="text-sm font-semibold text-forest">{{ review.name }}</p>
              <p class="text-xs text-mute">{{ review.place }}</p>
            </div>
          </div>
        </li>
      </ul>

      <div class="mt-8 flex items-center justify-center gap-2" role="tablist" aria-label="Opiniones">
        <button
          v-for="(_, index) in reviews"
          :key="index"
          type="button"
          role="tab"
          class="h-2.5 rounded-full transition-all"
          :class="page === index ? 'w-2.5 bg-forest' : 'w-2.5 border border-forest bg-transparent'"
          :aria-selected="page === index"
          :aria-label="`Opiniones, grupo ${index + 1}`"
          @click="page = index"
        />
      </div>

      <ul class="mx-auto mt-20 grid max-w-4xl gap-10 sm:grid-cols-3">
        <li v-for="benefit in benefits" :key="benefit.title" class="flex flex-col items-center text-center">
          <span class="grid h-14 w-14 place-items-center rounded-full bg-forest-soft text-forest">
            <svg v-if="benefit.icon === 'tag'" viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
              <path stroke-linejoin="round" d="M12 3H5v7l8.5 8.5a2 2 0 0 0 2.8 0L20.5 14a2 2 0 0 0 0-2.8L12 3z" />
              <circle cx="8.5" cy="8.5" r="1" fill="currentColor" stroke="none" />
            </svg>
            <svg v-else-if="benefit.icon === 'truck'" viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
              <path stroke-linejoin="round" d="M3 7h11v8H3zM14 10h4l3 3v2h-7" />
              <circle cx="7" cy="17.5" r="1.5" />
              <circle cx="17" cy="17.5" r="1.5" />
            </svg>
            <svg v-else viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
              <path stroke-linejoin="round" d="M12 3 5 6v6c0 4.2 2.8 7.2 7 8.5 4.2-1.3 7-4.3 7-8.5V6l-7-3z" />
              <path stroke-linecap="round" d="m9 12 2 2 4-4" />
            </svg>
          </span>
          <h3 class="mt-4 text-sm font-semibold text-forest">{{ benefit.title }}</h3>
          <p class="mt-1 max-w-[15rem] text-xs leading-relaxed text-mute">{{ benefit.text }}</p>
        </li>
      </ul>
    </div>
  </section>
</template>
