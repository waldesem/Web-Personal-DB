<script setup lang="ts" />

<template>
  <UCard
    :ui="{
      body: {
        padding: 'px-4 py-5 sm:p-4',
      },
      header: {
        padding: 'px-4 py-5 sm:p-4',
      },
      footer: {
        padding: 'px-4 py-4 sm:p-1',
      },
    }"
  >
    <template v-if="$slots.header" #header><slot name="header" /></template>
    <slot />
    <template v-if="$slots.footer" #footer><slot name="footer" /></template>
  </UCard>
</template>
