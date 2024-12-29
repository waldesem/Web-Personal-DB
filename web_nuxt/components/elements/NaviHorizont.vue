<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["delete", "update"]);

const props = defineProps({
  candId: {
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
  for (const file of files) {
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      toast.add({
        icon: "i-heroicons-exclamation-triangle",
        title: "Внимание",
        description: "Размер одного файла не должен превышать 10 МБ",
        color: "red",
      });
      continue;
    }
    formData.append("file", file);
  }
  const { message } = await authFetch(`/route/anketa/files/${props.item}/${props.candId}`, {
    method: "POST",
    body: formData,
  }) as Record<string, string>;
  if (message !== "success") {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Загрузка не удалась или отсутствует доступ к папке",
      color: "red",
    });
  } else {
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
    label: "Удалить",
    icon: "i-heroicons-trash",
    click: () => emit("delete"),
  },
  {
    label: "Изменить",
    icon: "i-heroicons-pencil-square",
    click: () => emit("update"),
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
  <UHorizontalNavigation :links="links" />
</template>
