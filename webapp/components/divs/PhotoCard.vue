<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import { useMouse, useWindowScroll } from "@vueuse/core";

const anketaState = stateAnketa();
const userState = stateUser();

const photoCard = ref({
  formData: new FormData(),

  submitImage(event: Event) {
    console.log(event.target);
    anketaState.submitFile(event, "image", anketaState.share.value.candId);
  },
  openFileForm(elementId: string) {
    document.getElementById(elementId)?.click();
  },
});

const { x, y } = useMouse();
const { y: windowY } = useWindowScroll();

const isOpen = ref(false);
const virtualElement = ref({ getBoundingClientRect: () => ({}) });

function onContextMenu() {
  const top = unref(y) - unref(windowY);
  const left = unref(x);

  virtualElement.value.getBoundingClientRect = () => ({
    width: 0,
    height: 0,
    top,
    left,
  });
  isOpen.value = true;
}
</script>

<template>
  <div class="flex justify-left">
    <div class="border rounded p-3" @contextmenu.prevent="onContextMenu">
      <NuxtImg
        :src="anketaState.share.value.imageUrl"
        width="240"
        height="240"
      />
      <UInput
        v-show="false"
        id="image-file"
        multiple
        type="file"
        accept="image/*"
        @change="photoCard.submitImage($event)"
      />
      <UContextMenu
        v-if="
          anketaState.anketa.value.persons['user_id'] ==
            userState.user.value.userId &&
          anketaState.anketa.value.persons['standing']
        "
        v-model="isOpen"
        :virtual-element="virtualElement"
      >
        <div class="p-4">
          <UButton
            label="Загрузить"
            variant="link"
            @click="photoCard.openFileForm('image-file')"
          />
        </div>
      </UContextMenu>
    </div>
  </div>
</template>
