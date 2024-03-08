<script setup lang="ts">
import { ref, onBeforeMount } from "vue";

const emit = defineEmits(["get-item", "submit-file"]);

onBeforeMount(() => {
  emit("get-item", "file")
});

const props = defineProps({
  imageUrl: String,
});

const photoCard = ref({
  formData: new FormData(),
  showPhoto: false,

  handleMouse: function () {
    this.showPhoto = !this.showPhoto;
  },
});

function submitFile (event: Event) {
  emit("submit-file", [event, "image"]);
};
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
        @change="submitFile($event)"
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
