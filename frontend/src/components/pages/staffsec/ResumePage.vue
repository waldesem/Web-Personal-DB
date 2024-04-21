<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { axiosAuth } from "@/auth";
import { stateAlert } from "@/state";
import { server } from "@/utilities";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("@components/content/forms/ResumeForm.vue")
);

const formData = ref(new FormData());

async function submitFile(event: Event): Promise<void> {
  const inputElement = event.target as HTMLInputElement;
  if (inputElement.files) {
    formData.value.append("file", inputElement.files[0]);
    try {
      const response = await axiosAuth.post(
        `${server}/file/anketa/0`,
        formData.value
      );
      const { message } = response.data;
      router.push({ name: "profile", params: { id: message } });

      stateAlert.setAlert(
        "alert-success",
        "Файл успешно загружен"
      );
    } catch (error) {
      console.error(error);
    }
  } else {
    stateAlert.setAlert(
      "alert-warning",
      "Ошибка при загрузке файла"
    );
  }
};
</script>

<template>
  <div class="row mb-5">
  <HeaderDiv :page-header="'Создать анкету'" />
  </div>
  <FileForm :accept="'.json'" @submit="submitFile" />
  <ResumeForm @cancel="router.push({ name: 'persons' })" />
</template>
