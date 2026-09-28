<script setup lang="ts">
defineProps<{
  variant: 'sand' | 'blue' | 'mint' | 'lilac'
}>()
</script>

<template>
  <svg viewBox="0 0 320 220" class="h-full w-full" aria-hidden="true">
    <rect width="320" height="220" fill="#F4EFE8" />
    <ellipse cx="160" cy="196" rx="86" ry="8" fill="#0A3D36" opacity="0.06" />

    <template v-if="variant === 'sand'">
      <g>
        <rect x="58" y="42" width="78" height="142" rx="8" fill="#E7D5C2" />
        <rect x="70" y="58" width="54" height="70" rx="5" fill="#D7B7C8" />
        <rect x="78" y="142" width="38" height="7" rx="2" fill="#CDB89F" />
        <rect x="78" y="156" width="28" height="5" rx="2" fill="#CDB89F" />
      </g>
      <g>
        <rect x="176" y="78" width="58" height="106" rx="18" fill="#FBF8F4" stroke="#E6DDD2" />
        <rect x="190" y="58" width="30" height="26" rx="5" fill="#D5CEC4" />
        <rect x="198" y="42" width="14" height="20" rx="4" fill="#C4BBB0" />
        <rect x="188" y="104" width="34" height="28" rx="4" fill="#EADFD4" />
      </g>
    </template>

    <template v-else-if="variant === 'blue'">
      <g>
        <rect x="62" y="40" width="84" height="146" rx="8" fill="#1E4C86" />
        <rect x="74" y="56" width="60" height="46" rx="4" fill="#2F6CB3" />
        <circle cx="104" cy="78" r="10" fill="#F7FBFF" opacity="0.9" />
        <rect x="78" y="118" width="48" height="6" rx="2" fill="#D6E6F7" />
        <rect x="78" y="132" width="36" height="5" rx="2" fill="#9EBFDF" />
        <rect x="78" y="158" width="28" height="8" rx="2" fill="#F4C56A" />
      </g>
      <g>
        <rect x="176" y="72" width="54" height="114" rx="16" fill="#F7FBFF" stroke="#D5E2EF" />
        <rect x="188" y="52" width="30" height="24" rx="6" fill="#1E4C86" />
        <rect x="190" y="98" width="26" height="34" rx="4" fill="#E5F0FA" />
      </g>
    </template>

    <template v-else-if="variant === 'mint'">
      <g>
        <rect x="78" y="48" width="164" height="124" rx="12" fill="#FBFBF9" stroke="#E4EBE6" />
        <rect x="78" y="48" width="164" height="36" rx="12" fill="#1F6B5A" />
        <rect x="78" y="72" width="164" height="12" fill="#1F6B5A" />
        <rect x="96" y="104" width="72" height="8" rx="2" fill="#D5E4DE" />
        <rect x="96" y="120" width="52" height="6" rx="2" fill="#E3EDE8" />
        <circle cx="206" cy="124" r="18" fill="#E7F2EE" />
        <path d="M206 114c4 4 6 8 6 12-6 2-12 2-16-2 2-6 6-10 10-10z" fill="#1F6B5A" />
      </g>
    </template>

    <template v-else>
      <g>
        <rect x="118" y="36" width="84" height="150" rx="28" fill="#CDB8D8" />
        <rect x="128" y="78" width="64" height="96" rx="22" fill="#B79AC6" />
        <rect x="140" y="22" width="40" height="22" rx="6" fill="#E7DDF0" />
        <rect x="152" y="12" width="16" height="14" rx="4" fill="#F4EEF8" />
        <rect x="136" y="96" width="48" height="36" rx="6" fill="#F7F3FA" opacity="0.85" />
        <path d="M146 36c18 8 28 28 24 70" fill="none" stroke="#F7F3FA" stroke-width="6" stroke-linecap="round" opacity="0.55" />
      </g>
    </template>
  </svg>
</template>
