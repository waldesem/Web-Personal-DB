<script setup lang="ts">
import { useFetchAuth } from "@/utils/auth";
import { useMouse, useWindowScroll } from "@vueuse/core";

const authFetch = useFetchAuth();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  destination: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const imageUrl = ref("");

const { refresh } = await useAsyncData("image", async () => {
  const response = await $fetch("/api/image", {
    params: {
      image: props.destination,
    },
    responseType: "blob",
  });
  imageUrl.value = window.URL.createObjectURL(new Blob([response] as never));
});

async function submitImage(file: File) {
  if (!file) return;
  const formData = new FormData();
  formData.append("file", file);
  await authFetch("/api/file/image/" + props.candId, {
    method: "POST",
    body: formData,
  });
  await refresh();
}

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}

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
      <NuxtImg :src="imageUrl" width="200" height="200" />
      <UInput
        v-show="false"
        id="image-file"
        type="file"
        accept="image/*"
        multiple
        @change="submitImage($event)"
      />
      <UContextMenu
        v-if="props.editable"
        v-model="isOpen"
        :virtual-element="virtualElement"
      >
        <div class="p-4">
          <UButton
            label="Загрузить"
            variant="link"
            @click="openFileForm('image-file')"
          />
        </div>
      </UContextMenu>
    </UCard>
  </div>
</template>
