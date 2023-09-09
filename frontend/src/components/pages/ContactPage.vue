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
    <h1>{{ `Сейчас ${clock} а страница все еще в разработке` }}</h1>
</template>

<style scoped>

.h1 {
    color: red;
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-top: 30px;
    margin-bottom: 30px;
}

</style>
