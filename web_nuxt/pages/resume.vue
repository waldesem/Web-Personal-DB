<script setup lang="ts">
function openProfile(candId: string) {
  return navigateTo("/profile/" + candId);
}

function openPersons() {
  return navigateTo("/persons");
}
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :div="'mb-6'" :header="'НОВАЯ АНКЕТА'" />
    <UCard>
      <FormsResumeForm @cancel="openPersons" @update="openProfile" />
    </UCard>
  </LayoutsMenu>
</template>
