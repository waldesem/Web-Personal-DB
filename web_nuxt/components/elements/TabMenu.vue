<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";

const toast = useToast();

const emit = defineEmits(["delete", "update"]);

const props = defineProps({
  item: {
    type: String,
    default: "",
  },
  candId: {
    type: String,
    required: true,
  },
});

const { open, reset, onCancel, onChange } = useFileDialog();

onChange(async (files) => {
  if (!files) return;
  const formData = new FormData();
  for (const file of files) {
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      makeToast("info", "Размер одного файла не должен превышать 10 МБ");
      continue;
    }
    formData.append("file", file);
  }
  const { message } = (await useFetchAuth(
    `/route/explorer/files/${props.item}/${props.candId}`,
    {
      method: "POST",
      body: formData,
    }
  )) as Record<string, string>;
  if (message == "success") {
    makeToast("success", "Файлы успешно загружены");
  } else {
    makeToast();
  }
  reset();
});

onCancel(() => {
  reset();
});

const items = [
  {
    label: "Изменить",
    icon: "i-heroicons-pencil-square",
    onSelect() {
      emit("update");
    },
  },
  {
    label: "Загрузить",
    icon: "i-heroicons-cloud-arrow-up",
    onSelect() {
      open();
    },
  },
  {
    label: "Удалить",
    icon: "i-heroicons-trash",
    onSelect() {
      emit("delete");
    },
  },
];
</script>

<template>
  <UDropdownMenu :items="items" :content="{ align: 'end' }">
    <UButton
      size="xl"
      color="neutral"
      icon="i-heroicons-ellipsis-vertical"
      variant="ghost"
      title="Выбор действия"
    />
  </UDropdownMenu>
</template>
