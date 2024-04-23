<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("@components/content/forms/ResumeForm.vue")
);
</script>

<template>
  <HeaderDiv :page-header="'Создать анкету'" />
  <ResumeForm @cancel="router.push({ name: 'persons' })" />
</template>
