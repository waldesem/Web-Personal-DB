<script setup lang="ts">
function openProfile(candId: string) {
  return navigateTo('/profile/' + candId)
}
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :div="'mb-6'" :header="'НОВАЯ АНКЕТА'"/>
    <UCard>
      <FormsResumeForm 
        @cancel="navigateTo('/persons')"
        @update="openProfile" />
    </UCard>
  </LayoutsMenu>
</template>
