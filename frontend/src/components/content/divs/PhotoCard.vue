<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import { stateAnketa, submitFile } from "@/state";

onBeforeMount(async () => {
  await stateAnketa.getItem("image");
});

const photoCard = ref({
  formData: new FormData(),
  showPhoto: false,

  handleMouse() {
    this.showPhoto = !this.showPhoto;
  },

  async submitImage(event: any) {
    await submitFile(event, "image");
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
      <img
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
          accept="image/jpg, image/jpeg"
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
