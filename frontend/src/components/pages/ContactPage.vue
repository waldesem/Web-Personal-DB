<script setup lang="ts">

import { ref } from 'vue';


const clock = ref('');

function updateClock() {
    // Get the current date and time
    const now = new Date();

    // Extract the hours, minutes, and seconds
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    // Format the time as HH:MM:SS
    clock.value = `${hours}:${minutes}:${seconds}`;
};

// Update the clock every second
setInterval(updateClock, 1000);

</script>

<template>
  <div class="container py-5">
    <div class="py-5" id="header">
      <h1 class="text-center">{{ clock }}</h1>
      <h2 class="text-center">Страница в разработке</h2>
      <h3 class="text-center">Приносим извинения за доставленные неудобства</h3>
      <h4 class="text-center">Благодарим за понимание</h4>
      <h5 class="text-center">Администрация</h5>
    </div>
  </div>
</template>
  