<script setup lang="ts">
const switchToPersons = () => {
  navigateTo('/persons');
}
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :div="'py-1'" :header="'НОВАЯ АНКЕТА'"/>
    <div class="border rounded p-5">
      <FormsResumeForm @cancel="switchToPersons"/>
    </div>
  </LayoutsMenu>
</template>
