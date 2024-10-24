<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";

const toast = useToast();


const emit = defineEmits(["delete", "update", "upgrade"]);

const props = defineProps({
  navlen: {
    type: Number,
    default: 4,
  },
  candId: {
    type: String,
    default: "",
  },
  inputId: {
    type: String,
    default: "",
  },
  item: {
    type: String,
    default: "",
  },
});

const { open, reset, onCancel, onChange } = useFileDialog();

onChange(async (files) => {
  if (!files) return;
  const formData = new FormData();
  if (files) {
    for (const file of files) {
      formData.append("file", file);
    }
    await useFetch(`/api/file/${props.item}/${props.candId}`, {
      method: "POST",
      body: formData,
    });
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: "Файлы успешно загружены",
      color: "green",
    });
  }
  reset();
});

onCancel(() => {
  reset();
});

const links = [
  {
    label: "Изменить",
    icon: "i-heroicons-pencil-square",
    click: () => emit("update"),
  },
  {
    label: "Удалить",
    icon: "i-heroicons-trash",
    click: () => emit("delete"),
  },
  {
    label: "Обновить",
    icon: "i-heroicons-arrow-path",
    click: () => emit("upgrade"),
  },
  {
    label: "Загрузить",
    icon: "i-heroicons-cloud-arrow-up",
    slot: "upload",
    click: () => open(),
  },
];
</script>

<template>
  <UHorizontalNavigation :links="links.slice(0, props.navlen)" />
</template>
