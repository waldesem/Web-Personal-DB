<script setup lang="ts">
const toast = useToast();

const authFetch = useFetchAuth();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  fullname: {
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
  accept: "image/*",
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
  const { message } = (await authFetch("/api/file/image/" + props.candId, {
    method: "POST",
    body: formData,
  })) as Record<string, string>;
  if (message == "success") {
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
});
</script>

<template>
  <div class="flex justify-left">
    <UButton variant="link" @click="open">
      <template #leading>
        <img
          :src="imageUrl"
          :alt="fullname"
          width="160"
          height="160"
          title="Загрузить"
        >
      </template>
    </UButton>
  </div>
</template>
