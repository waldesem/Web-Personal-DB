<script setup lang="ts">
const personState = statePersons();



const switchToPersons = async() => {
  navigateTo('/persons');
  await personState.getCandidates();
}
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :div="'mb-6'" :header="'НОВАЯ АНКЕТА'"/>
    <UCard>
      <FormsResumeForm @cancel="switchToPersons"/>
    </UCard>
  </LayoutsMenu>
</template>
