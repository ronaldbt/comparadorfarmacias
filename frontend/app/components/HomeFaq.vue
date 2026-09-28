<script setup lang="ts">
const items = [
  {
    id: 'como',
    question: '¿Cómo funciona el comparador?',
    answer: 'Indicas el medicamento y reunimos precios de farmacias cercanas. Ves el más bajo, el tiempo de entrega y si hay stock, y eliges dónde comprar.'
  },
  {
    id: 'actualizado',
    question: '¿Los precios están al día?',
    answer: 'Se actualizan varias veces al día con la información que publica cada farmacia. El valor final puede cambiar si hay un descuento en caja.'
  },
  {
    id: 'comprar',
    question: '¿Puedo comprar directo en Salvia?',
    answer: 'Salvia compara. La compra se hace en la farmacia que elijas, en su sitio o en el local. No cobramos comisión al paciente.'
  },
  {
    id: 'costo',
    question: '¿Tiene costo usar Salvia?',
    answer: 'No. Buscar y comparar es gratis. Solo pagas el medicamento en la farmacia que elijas.'
  },
  {
    id: 'stock',
    question: '¿Qué pasa si el producto no tiene stock?',
    answer: 'Lo marcamos como agotado y te mostramos equivalentes con el mismo principio activo, para que no te quedes sin opción.'
  }
]

const openId = ref('como')

function toggle(id: string) {
  openId.value = openId.value === id ? '' : id
}
</script>

<template>
  <section id="preguntas" class="scroll-mt-24 px-4 py-4 sm:px-6 md:py-8">
    <div class="mx-auto max-w-3xl rounded-[2rem] bg-fog px-4 py-12 sm:px-10 md:py-14">
      <h2 class="text-center font-serif text-3xl tracking-tight text-forest sm:text-4xl">
        Preguntas frecuentes
      </h2>
      <p class="mx-auto mt-3 max-w-md text-center text-sm leading-relaxed text-mute">
        Respuestas claras para comparar con tranquilidad, antes de elegir farmacia.
      </p>

      <ul class="mt-8 space-y-3">
        <li
          v-for="item in items"
          :key="item.id"
          class="overflow-hidden rounded-2xl transition-colors"
          :class="openId === item.id ? 'bg-forest text-white' : 'bg-white text-forest shadow-sm'"
        >
          <button
            type="button"
            class="flex w-full items-center justify-between gap-4 px-5 py-4 text-left text-sm font-medium"
            :aria-expanded="openId === item.id"
            :aria-controls="`respuesta-${item.id}`"
            @click="toggle(item.id)"
          >
            <span>{{ item.question }}</span>
            <svg viewBox="0 0 24 24" class="h-4 w-4 shrink-0" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path v-if="openId !== item.id" stroke-linecap="round" d="M12 5v14M5 12h14" />
              <path v-else stroke-linecap="round" d="M5 12h14" />
            </svg>
          </button>
          <div
            :id="`respuesta-${item.id}`"
            class="grid transition-[grid-template-rows] duration-300 ease-out"
            :class="openId === item.id ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
          >
            <div class="overflow-hidden">
              <p class="px-5 pb-5 text-sm leading-relaxed text-white/80">
                {{ item.answer }}
              </p>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </section>
</template>
