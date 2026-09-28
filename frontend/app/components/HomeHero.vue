<template>
  <section id="inicio" class="scroll-mt-28 px-4 pt-5 sm:px-6">
    <div class="mx-auto grid w-full min-w-0 max-w-6xl overflow-hidden rounded-[1.75rem] bg-forest md:min-h-[440px] md:grid-cols-[1.05fr_0.95fr]">
      <div class="flex min-w-0 flex-col justify-center px-6 py-10 sm:px-10 lg:px-14">
        <h1 class="max-w-full text-[1.85rem] font-semibold leading-[1.08] tracking-tight text-white sm:text-5xl">
          Todo lo que necesitas para la temporada de resfrío
        </h1>
        <p class="mt-4 max-w-full text-sm leading-relaxed text-white/80 sm:max-w-sm sm:text-base">
          Alivio efectivo, con precios de varias farmacias. Encuentra lo que te hace falta sin dar vueltas.
        </p>
        <a
          href="#productos"
          class="mt-7 inline-flex w-fit items-center gap-2 rounded-full bg-[#F5C518] px-5 py-2.5 text-sm font-semibold text-forest transition-colors hover:bg-[#E6B40C]"
        >
          Ver todo
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path stroke-linecap="round" d="M5 12h14M13 6l6 6-6 6" />
          </svg>
        </a>
      </div>
      <div class="relative min-h-[280px] min-w-0 overflow-hidden">
        <img
          src="/images/hero.jpg"
          alt="Farmacéutico con bata blanca"
          class="h-72 w-full object-cover object-top md:absolute md:inset-0 md:h-full"
        >
      </div>
    </div>
  </section>
</template>
