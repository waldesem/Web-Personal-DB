<script setup lang="ts">
const router = useRouter();
</script>

<template>
  <LayoutsStaffsec>
  <ElementsHeaderDiv :page-header="'Создать анкету'"/>
  <FormsResumeForm @cancel="router.push({ name: 'persons' })"/>
  </LayoutsStaffsec>
</template>
