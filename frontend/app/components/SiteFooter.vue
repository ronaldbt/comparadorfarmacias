<script setup lang="ts">
const route = useRoute()
const anchoPagina = computed(() => route.path === '/remedios' ? 'max-w-[1480px]' : 'max-w-6xl')
</script>

<template>
  <footer id="contacto" class="scroll-mt-24 px-4 pb-6 pt-4 sm:px-6 lg:px-8">
    <div class="mx-auto rounded-[1.75rem] bg-forest px-6 py-10 text-white/75 sm:px-10 sm:py-12" :class="anchoPagina">
      <div class="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <p class="font-serif text-3xl text-white">Salvia</p>
          <p class="mt-3 max-w-xs text-sm leading-relaxed">
            Compara precios de medicamentos y elige la farmacia que te queda mejor: más cerca, con despacho o al menor valor.
          </p>
        </div>

        <div>
          <p class="text-sm font-medium text-white">Páginas</p>
          <ul class="mt-3 space-y-2 text-sm">
            <li><a href="#inicio" class="transition-colors hover:text-white">Inicio</a></li>
            <li><a href="#productos" class="transition-colors hover:text-white">Medicamentos</a></li>
            <li><a href="#simple" class="transition-colors hover:text-white">Cómo funciona</a></li>
            <li><a href="#preguntas" class="transition-colors hover:text-white">Preguntas</a></li>
          </ul>
        </div>

        <div>
          <p class="text-sm font-medium text-white">Compañía</p>
          <ul class="mt-3 space-y-2 text-sm">
            <li><a href="#contacto" class="transition-colors hover:text-white">Farmacias</a></li>
            <li><a href="#simple" class="transition-colors hover:text-white">Cómo trabajamos</a></li>
            <li><a href="#contacto" class="transition-colors hover:text-white">Contacto</a></li>
            <li><a href="#preguntas" class="transition-colors hover:text-white">Ayuda</a></li>
          </ul>
        </div>

        <div>
          <p class="text-sm font-medium text-white">Contacto</p>
          <ul class="mt-3 space-y-2 text-sm">
            <li><a href="mailto:hola@salvia.app" class="transition-colors hover:text-white">hola@salvia.app</a></li>
            <li>Lunes a viernes, 9:00 a 18:00</li>
            <li>Respuesta en el mismo día</li>
          </ul>
        </div>
      </div>

      <div class="mt-10 flex flex-col gap-3 border-t border-white/10 pt-6 text-xs sm:flex-row sm:items-center sm:justify-between">
        <p>© 2026 Salvia. Todos los derechos reservados.</p>
        <div class="flex flex-wrap gap-x-4 gap-y-1">
          <a href="#contacto" class="transition-colors hover:text-white">Privacidad</a>
          <a href="#contacto" class="transition-colors hover:text-white">Términos</a>
          <a href="#contacto" class="transition-colors hover:text-white">Aviso legal</a>
        </div>
      </div>
    </div>
  </footer>
</template>
