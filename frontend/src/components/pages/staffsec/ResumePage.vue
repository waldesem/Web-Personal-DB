<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server } from "@/utilities/utils";
import { router } from "@/router/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("@components/content/forms/ResumeForm.vue")
);

const storeAuth = authStore();
const storeAlert = alertStore();

const dataJson = ref({
  formData: new FormData(),
});

function switchToProfile(idx: string): void {
  router.push({ name: "profile", params: { id: idx } });
};

async function submitFile(event: Event): Promise<void> {
  const inputElement = event.target as HTMLInputElement;
  if (inputElement && inputElement.files && inputElement.files.length) {
    dataJson.value.formData.append("file", inputElement.files[0]);
    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/file/anketa/0`,
        dataJson.value.formData
      );
      const { message } = response.data;
      switchToProfile(message);

      storeAlert.alertMessage.setAlert(
        "alert-success",
        "Файл успешно загружен"
      );
    } catch (error) {
      console.error(error);
    }
  } else {
    storeAlert.alertMessage.setAlert(
      "alert-warning",
      "Ошибка при загрузке файла"
    );
  }
};
</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Создать анкету'" />
    <FileForm
      :accept="'.json'"
      @submit="submitFile"
    />
    <ResumeForm 
      @submit="switchToProfile"/>
  </div>
</template>
