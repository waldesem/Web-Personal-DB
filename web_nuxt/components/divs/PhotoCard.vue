<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import { useMouse, useWindowScroll } from "@vueuse/core";

const anketaState = stateAnketa();

await anketaState.getImage();

const photoCard = ref({
  formData: new FormData(),

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

const editState = inject("editState") as boolean
</script>

<template>
  <div class="flex justify-left">
    <UCard 
      @contextmenu.prevent="onContextMenu"
    >
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
        @change="
          anketaState.submitFile(
            $event,
            'image',
            anketaState.share.value.candId
          )
        "
      />
      <UContextMenu
        v-if="editState"
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
    </UCard>
  </div>
</template>
