<script setup lang="ts">
import type { Files, Folders } from "@/types";

const user = useUserState();
const person = usePersonState();

const fullPath = ref(person.value.destination) as Ref<string>;
const listFolders = ref<Folders[]>([]);
const listFiles = ref<Files[]>([]);

const { status } = await useLazyAsyncData(
  "explorer",
  async () => {
    const { path, folders, files } = (await fetchAuth(
      "/route/explorer/folder/" + person.value.id,
      {
        params: {
          path: fullPath.value,
        },
      }
    )) as {
      path: string;
      folders: Folders[];
      files: Files[];
    };
    if (path !== fullPath.value) fullPath.value = path;
    listFolders.value = folders;
    listFiles.value = files;
  },
  { watch: [fullPath] }
);

async function openFile(path: string, name: string) {
  status.value = "pending";
  const file = (await fetchAuth("/route/explorer/file", {
    params: {
      path: path,
    },
  })) as Blob;
  status.value = "success";
  const url = URL.createObjectURL(file);
  const link = document.createElement("a");
  link.style.display = "none";
  link.href = url;
  link.download = name;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
</script>

<template>
  <div class="flex flex-col p-2">
    <UButton
      :loading="status == 'pending'"
      label="Домой"
      variant="ghost"
      size="xl"
      icon="i-heroicons-home"
      @click="fullPath = person.destination"
    />
    <div v-if="status === 'pending'">
      <div v-for="i in listFolders.length + listFiles.length + 1" :key="i">
        <div class="my-3">
          <USkeleton class="h-6 w-[600px]" />
        </div>
      </div>
    </div>
    <div v-else-if="listFolders.length == 0 && listFiles.length == 0">
      <div class="text-center text-red-800 my-3">Пустая папка</div>
    </div>
    <div v-else style="overflow: auto">
      <div v-for="folder in listFolders" :key="folder.name">
        <UButton
          :label="
            folder.name.length < 64
              ? folder.name
              : folder.name.slice(0, 64) + '...'
          "
          icon="i-heroicons-folder"
          variant="ghost"
          size="xl"
          :title="folder.name"
          @click="fullPath = folder.path"
        />
      </div>
      <div v-for="file in listFiles" :key="file.name">
        <UButton
          :disabled="user.role !== 'user'"
          :label="
            file.name.length < 64 ? file.name : file.name.slice(0, 64) + '...'
          "
          icon="i-heroicons-document"
          variant="ghost"
          size="xl"
          :title="file.name"
          @click="openFile(file.path, file.name)"
        />
      </div>
    </div>
  </div>
  <USeparator class="my-4" />
  <div class="text-sm text-center break-all">{{ fullPath }}</div>
</template>
