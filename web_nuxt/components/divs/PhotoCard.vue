<script setup lang="ts">
import { useMouse, useWindowScroll } from "@vueuse/core";

const toast = useToast();

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

const { open, reset, onCancel, onChange } = useFileDialog({
  accept: ".json",
  multiple: false,
});

onCancel(() => {
  reset();
});

onChange(async (files) => {
  if (!files) return;
  const formData = new FormData();
  const file = files[0];
  formData.append("file", file);
  const { message } = await authFetch("/api/file/image/" + props.candId, {
    method: "POST",
    body: formData,
  }) as Record<string, string>;
  if (message == 'success') {
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Успешно",
      description: "Фото добавлено",
      color: "green",
    });
  } else {
    toast.add({
      icon: "i-heroiconsi-heroicons-information-circle",
      title: "Внимание",
      description: "Ошибка формата",
      color: "red",
    });
  }
  reset();
  await refresh();
})

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
    <ElementsCardDiv
      :ui="{ body: { padding: 'p-1 sm:p-1' } }"
      @contextmenu.prevent="onContextMenu"
    >
      <NuxtImg :src="imageUrl" width="180" height="180" />
      <UContextMenu
        v-if="props.editable"
        v-model="isOpen"
        :virtual-element="virtualElement"
      >
        <UButton
          label="Загрузить"
          variant="link"
          @click="open"
        />
      </UContextMenu>
    </ElementsCardDiv>
  </div>
</template>
