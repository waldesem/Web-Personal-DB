<script setup lang="ts">
import { server, stateAnketa } from "@/state/state";
import { useFetchAuth } from "@/utils/auth";
import { useMouse, useWindowScroll } from "@vueuse/core";

const authFetch = useFetchAuth();

const editState = inject("editState") as boolean;

const anketaState = stateAnketa();

const imageUrl = ref("");

// const { refresh } = await useAsyncData("image", async () => {
//   const response = await $fetch(`${server}/image`, {
//     params: {
//       image: anketaState.anketa.value.persons.destination,
//     },
//     responseType: "blob",
//   });
//   imageUrl.value = window.URL.createObjectURL(new Blob([response] as never));
// });

const { data, refresh } = await useFetch(`${server}/image`, {
  params: {
    image: anketaState.anketa.value.persons.destination,
  },
  responseType: "blob",
});
imageUrl.value = window.URL.createObjectURL(new Blob([data] as never));

async function submitImage(fileList: FileList) {
  const toast = useToast();
  if (!fileList.length) {
    toast.add({
      icon: "i-heroicons-exclamation-triangle",
      title: "Информация",
      description: `Не выбраны файлы`,
      color: "red",
    });
    return;
  }
  const formData = new FormData();
  for (const file of fileList) {
    formData.append("file", file);
  }
  await authFetch(`${server}/file/image/${anketaState.share.value.candId}`, {
    method: "POST",
    body: formData,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: `Файлы успешно загружены`,
    color: "green",
  });
  await refresh();
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
      :ui="{ body: { padding: 'p-1 sm:p-1' } }"
      @contextmenu.prevent="onContextMenu"
    >
      <NuxtImg :src="imageUrl" width="240" height="240" />
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
