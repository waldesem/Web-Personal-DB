<script setup lang="ts">

const switchToPersons = async() => {
  navigateTo('/persons');
};
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :div="'mb-6'" :header="'НОВАЯ АНКЕТА'"/>
    <UCard>
      <FormsResumeForm @cancel="switchToPersons"/>
    </UCard>
  </LayoutsMenu>
</template>
