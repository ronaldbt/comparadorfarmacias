<script setup lang="ts">
const { topic } = useCatalog()

const categories = [
  { label: 'Día a día', topic: 'alergia' as const, icon: 'everyday' },
  { label: 'Vitaminas', topic: 'solar' as const, icon: 'vitamins' },
  { label: 'Primeros auxilios', topic: 'alergia' as const, icon: 'aid' },
  { label: 'Cuidado personal', topic: 'hidratacion' as const, icon: 'care' },
  { label: 'Salud femenina', topic: 'hidratacion' as const, icon: 'women' },
  { label: 'Bebé', topic: 'solar' as const, icon: 'baby' }
]

function choose(next: typeof categories[number]['topic']) {
  topic.value = next
  document.getElementById('productos')?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <section id="categorias" class="scroll-mt-28 px-4 py-8 sm:px-6">
    <ul class="mx-auto grid max-w-6xl grid-cols-3 gap-4 sm:grid-cols-6">
      <li v-for="category in categories" :key="category.label">
        <button type="button" class="group flex w-full flex-col items-center gap-3" @click="choose(category.topic)">
          <span class="grid aspect-square w-full place-items-center rounded-2xl bg-[#F3F0EA] transition-colors group-hover:bg-[#E7F2EE]">
            <svg v-if="category.icon === 'everyday'" viewBox="0 0 64 64" class="h-12 w-12" aria-hidden="true">
              <rect x="18" y="14" width="16" height="36" rx="4" fill="#E24B4B" />
              <rect x="30" y="22" width="16" height="28" rx="8" fill="#7EC8E3" />
              <rect x="22" y="20" width="8" height="6" rx="1" fill="#fff" opacity=".8" />
            </svg>
            <svg v-else-if="category.icon === 'vitamins'" viewBox="0 0 64 64" class="h-12 w-12" aria-hidden="true">
              <rect x="24" y="12" width="16" height="40" rx="8" fill="#F4F7FB" stroke="#D5DDE8" />
              <rect x="28" y="8" width="8" height="8" rx="2" fill="#2F6B4F" />
              <rect x="28" y="26" width="8" height="12" rx="2" fill="#D9E8DF" />
            </svg>
            <svg v-else-if="category.icon === 'aid'" viewBox="0 0 64 64" class="h-12 w-12" aria-hidden="true">
              <rect x="12" y="22" width="40" height="28" rx="6" fill="#E24B4B" />
              <rect x="18" y="16" width="16" height="10" rx="3" fill="#C73838" />
              <rect x="29" y="30" width="6" height="14" rx="1" fill="#fff" />
              <rect x="25" y="34" width="14" height="6" rx="1" fill="#fff" />
            </svg>
            <svg v-else-if="category.icon === 'care'" viewBox="0 0 64 64" class="h-12 w-12" aria-hidden="true">
              <rect x="26" y="10" width="12" height="10" rx="3" fill="#F2C14E" />
              <rect x="20" y="20" width="24" height="32" rx="8" fill="#F7F1E6" stroke="#E6D7C4" />
              <rect x="26" y="30" width="12" height="10" rx="2" fill="#E7B8C8" />
            </svg>
            <svg v-else-if="category.icon === 'women'" viewBox="0 0 64 64" class="h-12 w-12" aria-hidden="true">
              <rect x="22" y="16" width="14" height="32" rx="6" fill="#F3D6E2" />
              <rect x="32" y="22" width="12" height="26" rx="6" fill="#E8A0C0" />
              <rect x="26" y="10" width="6" height="8" rx="2" fill="#C97B9A" />
            </svg>
            <svg v-else viewBox="0 0 64 64" class="h-12 w-12" aria-hidden="true">
              <rect x="14" y="20" width="36" height="26" rx="6" fill="#7EB6E0" />
              <rect x="18" y="16" width="12" height="8" rx="2" fill="#F7C9D4" />
              <circle cx="40" cy="30" r="5" fill="#F8E7A2" />
            </svg>
          </span>
          <span class="text-center text-sm font-medium text-ink">{{ category.label }}</span>
        </button>
      </li>
    </ul>
  </section>
</template>
