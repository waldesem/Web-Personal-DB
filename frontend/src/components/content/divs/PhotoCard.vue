<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import { stateAnketa, submitFile } from "@/state";

onBeforeMount(async () => {
  await stateAnketa.getItem("image");
});

const photoCard = ref({
  formData: new FormData(),
  showPhoto: false,
  spinner: false,

  handleMouse() {
    this.showPhoto = !this.showPhoto;
  },

  async submitImage(event: any) {
    this.spinner = true;
    await submitFile(event, "image");
    this.spinner = false;
  },
});
</script>

<template>
  <div class="card mb-3" style="width: 16rem">
    <div
      class="card-img-container"
      @mouseover="photoCard.handleMouse"
      @mouseout="photoCard.handleMouse"
    >
      <span v-if="photoCard.spinner" class="spinner-border"></span>
      <img v-else
        :src="stateAnketa.share.imageUrl"
        style="width: 100%; height: auto"
        class="card-img-top"
        alt="..."
      />
      <div
        v-show="photoCard.showPhoto" 
        class="card-img-overlay"
      >
        <input
          @change="photoCard.submitImage($event)"
          class="form-control form-control-sm"
          id="formImage"
          type="file"
          accept="image/png, image/jpg, image/jpeg"
        />
      </div>
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
