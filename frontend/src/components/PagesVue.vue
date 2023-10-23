<template>
  <div class="container py-3">
    <router-view v-slot="{ Component }" >
      <transition name="component-fade" mode="out-in">
        <component :is="Component" :key="$route.fullPath"/>
      </transition>
    </router-view>
  </div>
</template>

<style scoped>

.component-fade-enter-active,
.component-fade-leave-active {
  transition: opacity 0.2s ease-in-out;
}

.component-fade-enter,
.component-fade-leave-to {
  opacity: 0;
}

</style>