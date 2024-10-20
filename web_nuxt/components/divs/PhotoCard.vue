<script setup lang="ts">
const authFetch = useFetchAuth();

const emit = defineEmits(["message"]);

const props = defineProps({
  candId: {
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
  const response = await $fetch("/api/image" + props.candId, {
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
  await refresh();
  emit("message", message);
  reset();
});
</script>

<template>
  <div class="flex justify-left">
    <UButton variant="link" :disabled="!editable" @click="open">
      <template #leading>
        <img :src="imageUrl" width="160" height="160" title="Загрузить фото" >
      </template>
    </UButton>
  </div>
</template>
