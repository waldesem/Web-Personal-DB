<script setup lang="ts">
import { ref, onBeforeMount, inject } from "vue";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

const storeAuth = authStore();
const storeAlert = alertStore();

onBeforeMount( async() => {
  await photoCard.value.getImage()
});

const photoCard = ref({
  candId: inject("candId") as string,
  formData: new FormData(),
  showPhoto: false,
  url: "",

  getImage: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/file/get/${this.candId}`,
        { responseType: "blob" }
      );
      this.url = window.URL.createObjectURL(new Blob([response.data]));
    } catch (error) {
      console.error(error);
    }
  },

  submitFile: async function (
    event: Event,
  ): Promise<void> {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files && inputElement.files.length > 0) {
      const maxSizeInBytes = 1024 * 1024; // 1MB
      if (inputElement.files[0].size > maxSizeInBytes) {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "File size exceeds the limit. Please select a smaller file."
        );
          inputElement.value = "";
          return;
        }
      try {
        const response = await storeAuth.axiosInstance.post(
          `${server}/file/image`,
          this.formData
        );
        const { message } = response.data;
        this.candId = message;
        this.getImage();

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

  handleMouse: function () {
    this.showPhoto = !this.showPhoto;
  },
});
</script>

<template>
  <div class="card" style="width: 16rem">
    <div
      class="card-img-container"
      @mouseover="photoCard.handleMouse"
      @mouseout="photoCard.handleMouse"
    >
      <img
        :src="photoCard.url ? photoCard.url : '/no-photo.png'"
        style="width: 100%; height: auto"
        class="card-img-top"
        alt="..."
      />
      <form
        :class="{ 'form-visible': photoCard.showPhoto }"
        @change="photoCard.submitFile($event)"
        class="form"
      >
        <input
          class="form-control form-control-sm"
          id="formImage"
          type="file"
          accept="image/png, image/jpg, image/jpeg"
        />
      </form>
    </div>
  </div>
</template>

<style scoped>
.card-img-container {
  position: relative;
  display: inline-block;
}

.form {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  visibility: hidden;
}

.form-visible {
  visibility: visible;
}
</style>
