<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server } from "@/utilities/utils";
import { router } from "@/router/router";

const HeaderDiv = defineAsyncComponent(
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
})
</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Создать анкету'" />
    <form
      class="form form-check"
      enctype="multipart/form-data"
      role="form"
      @change="dataJson.submitFile($event)"
    >
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
        <div class="col-lg-10">
          <input
            class="form-control"
            id="file"
            type="file"
            accept=".json"
            ref="file"
          />
        </div>
      </div>
    </form>
    <ResumeForm />
  </div>
</template>
@/store/auth