<script setup lang="ts">
import { ref, onBeforeMount } from "vue";

onBeforeMount( async() => {
  await props.getItem("file")
});

const props = defineProps({
  candId: String,
  imageUrl: String,
  getItem: {
    type: Function,
    required: true,
  },
  submitFile: {
    type: Function,
    required: true,
  },
});

const photoCard = ref({
  formData: new FormData(),
  showPhoto: false,

  submitFile: function (
    event: Event,
  ): void {
    props.submitFile(event, "image");
    props.getItem("file");
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
        :src="props.imageUrl ? props.imageUrl : '/no-photo.png'"
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
