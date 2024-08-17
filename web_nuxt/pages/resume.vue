<script setup lang="ts">
const switchToPersons = () => {
  navigateTo('/persons');
}
</script>

<template>
  <LayoutsMenu>
    <div class="py-8">
      <h3 class="text-2xl text-opacity-75 text-red-800 font-bold">
        Создать анкету
      </h3>
    </div>
    <div class="border rounded p-5">
      <FormsResumeForm @cancel="switchToPersons"/>
    </div>
  </LayoutsMenu>
</template>
