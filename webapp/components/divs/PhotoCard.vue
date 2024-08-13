<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";

const anketaState = stateAnketa();
const userState = stateUser();

const photoCard = ref({
  formData: new FormData(),
  showPhoto: false,

  async submitImage(event: Event) {
    await anketaState.submitFile(
      event,
      "image",
      anketaState.share.value.candId
    );
  },
});
</script>

<template>
  <div class="flex justify-left">
    <div
      class="border rounded p-3"
      @mouseover="photoCard.showPhoto = true"
      @mouseout="photoCard.showPhoto = false"
    >
      <NuxtImg
        :src="anketaState.share.value.imageUrl"
        width="240"
        height="240"
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
