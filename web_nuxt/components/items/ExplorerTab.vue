<script setup lang="ts">
import type { Files, Folders } from "@/types";

const user = useUserState();

const candId = inject("candId") as Ref<string>;

const fullPath = ref("") as Ref<string>;
const listFolders = ref<Folders[]>([]);
const listFiles = ref<Files[]>([]);

const { status } = await useLazyAsyncData(
  "explorer",
  async () => {
    const { path, folders, files } = (await fetchAuth(
      "/route/explorer/folder/" + candId.value,
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
      @click="fullPath = ''"
    />
    <div v-if="status === 'pending'">
      <div v-for="i in listFolders.length + listFiles.length + 1" :key="i">
        <div class="my-3">
          <USkeleton class="h-6 w-[300]" />
        </div>
      </div>
    </div>
    <div v-else-if="listFolders.length == 0 && listFiles.length == 0">
      <div class="text-center text-red-800 my-4">Пустая папка</div>
      <UIcon name="i-heroicons-folder-minus" class="size-12" />
    </div>
    <div v-else>
      <div v-for="(dir, index) in listFolders" :key="index">
        <UButton
          :label="
            dir.name.length < 64 ? dir.name : dir.name.slice(0, 64) + '...'
          "
          icon="i-heroicons-folder"
          variant="link"
          size="xl"
          :title="dir.name"
          @click="fullPath = dir.path"
        />
        <USeparator v-if="index != listFolders.length - 1" type="dashed" />
      </div>
      <USeparator v-if="listFolders.length && listFiles.length" type="dashed" />
      <div v-for="(file, index) in listFiles" :key="index">
        <UButton
          :disabled="user.role !== 'user'"
          :label="
            file.name.length < 64 ? file.name : file.name.slice(0, 64) + '...'
          "
          icon="i-heroicons-document"
          variant="link"
          size="xl"
          :title="file.name"
          @click="openFile(file.path, file.name)"
        />
        <USeparator v-if="index != listFolders.length - 1" type="dashed" />
      </div>
    </div>
  </div>
  <USeparator class="mt-4" />
  <div class="text-sm text-center break-all">{{ fullPath }}</div>
</template>
