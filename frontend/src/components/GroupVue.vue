<template>
  <router-view v-slot="{ Component }" >
    <transition name="component-fade" mode="out-in">
      <component :is="Component" :key="$route.fullPath"/>
    </transition>
  </router-view>
</template>

<style scoped>

.component-fade-enter-active,
.component-fade-leave-active {
  transition: opacity 0.1s ease-in-out; /* Adjust the duration as desired */
}

.component-fade-enter,
.component-fade-leave-to {
  opacity: 0;
}
</style>