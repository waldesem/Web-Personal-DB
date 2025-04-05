<script setup lang="ts">
import type { Files, Folders } from "@/types";

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;

const listFolders = ref<string[]>([]);
const listFiles = ref<string[]>([]);
const pending = ref(false);

const { refresh, status } = await useLazyAsyncData("explorer", async () => {
  const { folders, files } = (await authFetch(
    "/route/explorer/home/" + candId.value
  )) as {
    folders: Folders[];
    files: Files[];
  };
  listFolders.value = folders;
  listFiles.value = files;
});

async function openFolder(path: string) {
  pending.value = true;
  const { folders, files } = (await authFetch(
    "/route/explorer/folder",
    {
      params: {
        path: path,
      }
    }
  )) as {
    folders: Folders[];
    files: Files[];
  };
  listFolders.value = folders;
  listFiles.value = files;
  pending.value = false;
}

async function openFile(path: string) {
  pending.value = true;
  const file = (await authFetch("/route/explorer/file", {
    params: {
      path: path,
    }
  })) as Blob;
  const url = URL.createObjectURL(file);
  window.open(url);
  pending.value = false;
}
</script>

<template>
  <div class="mb-3">
    <UButton
      label="Домашняя папка"
      variant="outline"
      icon="i-heroicons-home"
      @click="refresh"
    />
  </div>
  <ElementsCardDiv>
    <div v-if="pending || status === 'pending'">
      <div
        v-for="i in listFolders.length + listFiles.length"
        :key="i"
        class="flex grid grid-cols-12 gap-3 mb-3"
      >
        <div class="col-span-3">
          <USkeleton class="h-4" />
        </div>
        <div class="col-span-9">
          <USkeleton class="h-4 w-[300px]" />
        </div>
      </div>
    </div>
    <div v-else>
      <div v-for="folder in listFolders" :key="folder" class="p-1">
        <UButton
          :label="folder.name"
          icon="i-heroicons-folder"
          variant="link"
          @click="openFolder(folder.path)"
        />
      </div>
      <div v-for="file in listFiles" :key="file" class="p-1">
        <UButton
          :label="file.name"
          icon="i-heroicons-document"
          variant="link"
          @click="openFile(file.path)"
        />
      </div>
    </div>
  </ElementsCardDiv>
</template>
