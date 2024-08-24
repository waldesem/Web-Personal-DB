<script setup lang="ts">
const switchToPersons = () => {
  navigateTo('/persons');
}
</script>

<template>
  <LayoutsMenu>
    <div class="my-14">
    <div class="border rounded p-5">
      <FormsResumeForm @cancel="switchToPersons"/>
    </div>
    </div>
  </LayoutsMenu>
</template>
