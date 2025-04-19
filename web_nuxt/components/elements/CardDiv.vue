<template>
  <UCard
    :ui="{
      footer: 'p-1',
    }"
  >
    <slot />
    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
  </UCard>
</template>
