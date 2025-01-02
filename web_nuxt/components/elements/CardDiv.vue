<template>
  <UCard
    :ui="{
      body: {
        padding: 'px-4 py-5',
      },
      header: {
        padding: 'px-4 py-5',
      },
      footer: {
        padding: 'px-4 py-4',
      },
    }"
  >
    <template v-if="$slots.header" #header>
      <slot name="header" />
    </template>
    <slot />
    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
  </UCard>
</template>
