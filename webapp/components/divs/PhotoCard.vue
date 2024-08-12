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
  <div class="flex relative">
    <div
      class="border rounded p-3"
      @mouseover="photoCard.handleMouse" @mouseout="photoCard.handleMouse">
      <NuxtImg 
        :src="anketaState.share.value.imageUrl"
        width="240" height="240" 
        />
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
  </div>
</template>
