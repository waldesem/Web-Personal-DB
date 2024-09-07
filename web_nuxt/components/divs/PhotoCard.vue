<script setup lang="ts">
import { server, stateAnketa } from "@/state/state";
import { useMouse, useWindowScroll } from "@vueuse/core";

const editState = inject("editState") as boolean;

const anketaState = stateAnketa();

const { data, refresh } = await useAsyncData("image", async () => {
  await $fetch(`${server}/image`, {
    params: {
      image: anketaState.anketa.value.persons.destination,
    },
    responseType: "blob",
  });
});

const imageUrl = ref(window.URL.createObjectURL(new Blob([data.value] as never)));

await refresh();

function submitImage(event: FileList) {
  anketaState.submitFile(event, "image", anketaState.share.value.candId);
  refresh();
}

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
</script>

<template>
  <div class="flex justify-left">
    <UCard 
      :ui = "{body: {padding: 'p-1 sm:p-6'}}"
      @contextmenu.prevent="onContextMenu"
      >
      <NuxtImg
        :src="imageUrl"
        width="240"
        height="240"
      />
      <UInput
        v-show="false"
        id="image-file"
        multiple
        type="file"
        accept="image/*"
        @change="submitImage($event)"
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
