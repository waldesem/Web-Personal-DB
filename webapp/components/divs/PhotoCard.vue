<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";

const anketaState = stateAnketa();
const userState = stateUser();

const photoCard = ref({
  formData: new FormData(),
  showPhoto: false,

  handleMouse() {
    this.showPhoto = !this.showPhoto;
  },

  async submitImage(event: any) {
    await anketaState.submitFile(
      event,
      "image",
      anketaState.share.value.candId
    );
  },
});
</script>

<template>
  <div class="border rounded">
    <div @mouseover="photoCard.handleMouse" @mouseout="photoCard.handleMouse">
      <NuxtImg :src="anketaState.share.value.imageUrl" alt="..." />
      <div
        v-show="
          photoCard.showPhoto &&
          anketaState.anketa.value.persons['user_id'] ==
            userState.user.value.userId &&
          anketaState.anketa.value.persons['standing']
        "
      >
        <UInput
          multiple
          type="file"
          accept="image/*"
          @change="photoCard.submitImage($event)"
        />
      </div>
  </div>
</div></template>

<!-- <style scoped>
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
</style> -->
