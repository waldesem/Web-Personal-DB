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
    await anketaState.submitFile(event, "image", anketaState.share.value.candId);
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
        :src="anketaState.share.value.imageUrl"
        style="width: 100%; height: auto"
        class="card-img-top"
        alt="..."
      />
      <div
        v-show="
          photoCard.showPhoto &&
          anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
          anketaState.anketa.value.persons['standing']
        "
        class="card-img-overlay"
      >
        <input
          @change="photoCard.submitImage($event)"
          class="form-control form-control-sm"
          id="formImage"
          type="file"
          accept="image/*"
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
