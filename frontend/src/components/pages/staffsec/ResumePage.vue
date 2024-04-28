<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { router } from "@/router";
import { axiosAuth } from "@/auth";
import { server } from "@/utilities";
import { stateAlert } from "@/state";

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
  <HeaderDiv :page-header="'Создать анкету'"/>
  <div class="position-relative">
    <div class="position-absolute bottom-100 end-0">
      <label for="file" class="text-primary">
        <i
          class="bi bi-cloud-arrow-down fs-1"
          title="Загрузить анкету"
          style="cursor: pointer"
        >
          </i>
      </label>
    <FileForm :accept="'.json'" @submit="submitFile"/>
    </div>  
  </div>
  <ResumeForm @cancel="router.push({ name: 'persons' })"/>
</template>
