<script setup lang="ts">
const router = useRouter();
</script>

<template>
  <LayoutsMenu>
  <ElementsHeaderDiv :page-header="'Создать анкету'"/>
  <FormsResumeForm @cancel="router.push('/persons')"/>
  </LayoutsMenu>
</template>
