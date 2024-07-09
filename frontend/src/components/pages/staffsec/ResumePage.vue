<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { router } from "@/router";
import { stateAnketa } from "@/state";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("@components/content/forms/ResumeForm.vue")
);
</script>

<template>
  <HeaderDiv :page-header="'Создать анкету'"/>
  <div class="position-relative">
    <div class="position-absolute bottom-100 end-0 px-3">
      <label
        for="file" 
        class="text-primary fs-5"
        style="cursor: pointer;"
      >Загрузить json
      &#9735;
      </label>
      <FileForm :accept="'.json'" @submit="stateAnketa.submitFile($event, 'persons', '0')" />
    </div>
  </div>
  <ResumeForm @cancel="router.push({ name: 'persons' })"/>
</template>
