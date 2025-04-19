<script setup lang="ts">
import type { Files, Folders } from "@/types";

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;

const listFolders = ref<Folders[]>([]);
const listFiles = ref<Files[]>([]);
const path = ref("") as Ref<string>;
const pending = ref(false);

const size = ref("lg") as Ref<"xs" | "sm" | "md" | "lg" | "xl">;

const { status } = await useLazyAsyncData(
  "explorer",
  async () => {
    const { folders, files } = (await authFetch(
      "/route/explorer/folder/" + candId.value,
      {
        params: {
          path: path,
        },
      }
    )) as {
      folders: Folders[];
      files: Files[];
    };
    listFolders.value = folders;
    listFiles.value = files;
  },
  { watch: [path] }
);

async function openFile(path: string, name: string) {
  pending.value = true;
  const file = (await authFetch("/route/explorer/file", {
    params: {
      path: path,
    },
  })) as Blob;
  pending.value = false;
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
  <ElementsCardDiv>
    <div class="flex justify-between">
      <UButton
        :loading="pending"
        label="Домашняя папка"
        variant="ghost"
        icon="i-heroicons-home"
        size="xl"
        @click="path = ''"
      />
      <USelectMenu
        v-model="size"
        variant="outline"
        :options="[
          { name: 'Самый маленькие', value: '2xs' },
          { name: 'Очень маленькие', value: 'xs' },
          { name: 'Маленькие значки', value: 'sm' },
          { name: 'Средние значки', value: 'md' },
          { name: 'Большие значки', value: 'lg' },
          { name: 'Очень большие', value: 'xl' },
        ]"
        option-attribute="name"
        value-attribute="value"
      />
    </div>
    <UDivider class="my-2" />
    <div v-if="pending || status === 'pending'">
      <div v-for="i in listFolders.length + listFiles.length" :key="i">
        <div class="my-3">
          <USkeleton class="h-6 w-[600px]" />
        </div>
      </div>
    </div>
    <div v-else-if="listFolders.length == 0 && listFiles.length == 0">
      <div class="text-center text-xl text-red-800 my-3">Пустая папка</div>
    </div>
    <div v-else style="overflow: auto">
      <div v-for="folder in listFolders" :key="folder.name">
        <UButton
          :disabled="stateUser.role != 'user'"
          :label="
            folder.name.length < 64
              ? folder.name
              : folder.name.slice(0, 64) + '...'
          "
          icon="i-heroicons-folder"
          variant="link"
          :size="size"
          :title="folder.name"
          @click="path = folder.path"
        />
      </div>
      <div v-for="file in listFiles" :key="file.name">
        <UButton
          :disabled="stateUser.role != 'user'"
          :label="
            file.name.length < 64 ? file.name : file.name.slice(0, 64) + '...'
          "
          icon="i-heroicons-document"
          variant="link"
          :size="size"
          :title="file.name"
          @click="openFile(file.path, file.name)"
        />
      </div>
    </div>
  </ElementsCardDiv>
</template>
