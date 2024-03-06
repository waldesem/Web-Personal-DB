<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server } from "@/utilities/utils";
import { router } from "@/router/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/ResumeForm.vue")
);

const storeAuth = authStore();
const storeAlert = alertStore();

const dataJson = ref({
  formData: new FormData(),

  submitFile: async function (
    event: Event,
  ): Promise<void> {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files && inputElement.files.length) {
      this.formData.append("file", inputElement.files[0]);
      try {
        const response = await storeAuth.axiosInstance.post(
          `${server}/file/anketa/0`,
          this.formData
        );
        const { message } = response.data;
        router.push({ name: "profile", params: { id: message } });

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
  },
});

function submitFile (event: Event){
  dataJson.value.submitFile(event)
};
</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Создать анкету'" />
    <FileForm
      :accept="'.json'"
      @submit="submitFile"
    />
    <ResumeForm />
  </div>
</template>
