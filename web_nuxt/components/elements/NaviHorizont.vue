<script setup lang="ts">
const emit = defineEmits(["delete", "update", "upload"]);

const props = defineProps({
  navlen: {
    type: Number,
    default: 3,
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
    label: "Загрузить",
    icon: "i-heroicons-cloud-arrow-up",
    slot: "upload",
    click: () => document.getElementById(props.inputId)?.click(),
  },
];

async function submitFile(fileList: FileList): Promise<void> {
  const formData = new FormData();
  if (fileList) {
    for (const file of fileList) {
      formData.append("file", file);
    }
    const response = await authFetch(
      `/api/file/${props.item}/${props.candId}`,
      {
        method: "POST",
        body: formData,
      }
    );
    console.log(response);
    toast.add({
      icon:
        response["message"] == "success"
          ? "i-heroicons-check-circle"
          : "i-heroicons-exclamation-triangle",
      title: response["message"] == "success" ? "Информация" : "Внимание",
      description:
        response["message"] == "success"
          ? "Файлы успешно загружены"
          : "Ошибка при загрузке файлов",
      color: response["message"] == "success" ? "green" : "red",
    });
  }
  formData.delete("file");
}
</script>

<template>
  <UHorizontalNavigation :links="links.slice(0, props.lastIndex)" />
  <div v-if="navlen == 3">
    <UInput
      v-show="false"
      :id="props.inputId"
      type="file"
      accept="*"
      multiple
      @change="submitFile($event)"
    />
  </div>
</template>
