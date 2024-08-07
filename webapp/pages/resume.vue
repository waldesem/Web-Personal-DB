<script setup lang="ts"></script>

<template>
  <LayoutsMenu>
  <ElementsHeaderDiv :page-header="'Создать анкету'"/>
  <FormsResumeForm @cancel="navigateTo('/persons')"/>
  </LayoutsMenu>
</template>
