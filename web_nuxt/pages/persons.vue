<script setup lang="ts">
import { debounce } from "@/utils/utilities";
import { useFetchAuth } from "../utils/auth";
import { server, stateClassify, stateUser } from "@/state/state";

const authFetch = useFetchAuth();

const classifyState = stateClassify();
const userState = stateUser();

const persons = ref({
  candidates: [] as Persons[],
  page: 1,
  prev: false,
  next: true,
  search: "",
  upload: false,
  updated: `${new Date().toLocaleDateString(
    "ru-RU"
  )} в ${new Date().toLocaleTimeString("ru-RU")}`,
});

const { refresh, status } = await useAsyncData("candidates", async () => {
  if (persons.value.page < 1) {
    persons.value.page = 1;
    return;
  }
  const response = await authFetch(`${server}/index/${persons.value.page}`, {
    params: {
      search: persons.value.search,
    },
  });
  
  [persons.value.candidates, persons.value.next, persons.value.prev] =
    response as [Persons[], boolean, boolean];

  persons.value.updated = `${new Date().toLocaleDateString(
    "ru-RU"
  )} в ${new Date().toLocaleTimeString("ru-RU")}`;
});

const searchPerson = debounce(async () => {
  await refresh();
}, 500);

const switchPage = async (page: number = 1) => {
  persons.value.page = page;
  await refresh();
};

async function uploadJson (fileList: FileList) {
  const toast = useToast();
  if (!fileList.length) {
    toast.add({
      icon: "i-heroicons-exclamation-triangle",
        title: "Внимание",
      description: `Файлы не выбраны`,
      color: "red",
    })
    return;
  };
  persons.value.upload = true;
  const formData = new FormData();
  for (const file of fileList) {
    formData.append("file", file);
  }
  const response = await authFetch(`${server}/file/persons/0`, {
    method: "POST",
    body: formData,
  });
  console.log(response);
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: `Файлы успешно загружены`,
    color: "green",
  });
  persons.value.upload = false;
  await refresh();
};
</script>

<template>
  <LayoutsMenu>
    <div
      v-if="
        userState.role == classifyState.classes.value.roles['user']
      "
      class="relative"
    >
      <div 
        class="absolute inset-y-0 right-0" 
        :class="{ 'animate-pulse': status == 'pending'|| persons.upload }"
        title="Загрузить json"
        >
        <UFormGroup class="mb-3" size="md">
          <template #label>
            <UIcon
              name="i-heroicons-cloud-arrow-up"
              class="w-8 h-8"
              style="cursor: pointer; color: dodgerblue"
            />
          </template>
          <UInput
            v-show="false"
            type="file"
            accept=".json"
            multiple
            @change="uploadJson($event)"
          />
        </UFormGroup>
      </div>
    </div>
    <ElementsHeaderDiv :header="'КАНДИДАТЫ'" />
    <div class="my-6">
      <UInput
        v-model="persons.search"
        placeholder="поиск по фамилии, имени, отчеству, дате рождения или инн"
        size="lg"
        @input.prevent="searchPerson"
      />
    </div>
    <UTable
      :loading="status == 'pending' || persons.upload"
      :progress="{ color: 'red', animation: 'swing' }"
      :empty-state="{
        icon: 'i-heroicons-circle-stack-20-solid',
        label: 'Ничего не найдено.',
      }"
      :columns="[
        { key: 'id', label: '#' },
        { key: 'region', label: 'Регион' },
        { key: 'surname', label: 'Фамилия Имя Отчество' },
        { key: 'birthday', label: 'Дата рождения' },
        { key: 'inn', label: 'ИНН' },
        { key: 'snils', label: 'СНИЛС' },
        { key: 'created', label: 'Обновлено' },
        { key: 'username', label: 'Сотрудник' },
        { key: 'editable', label: 'Статус' },
      ]"
      :rows="persons.candidates"
    >
      <template #id-data="{ row }">{{ row.id }}</template>
      <template #region-data="{ row }">{{ row.region }}</template>
      <template #surname-data="{ row }">
        <NuxtLink :to="`/profile/${row.id}`">
          {{
            `${row.surname} ${row.firstname} ${
              row.patronymic ? row.patronymic : ""
            }`
          }}
        </NuxtLink>
      </template>
      <template #birthday-data="{ row }">{{
        new Date(row.birthday).toLocaleDateString()
      }}</template>
      <template #birthplace-data="{ row }">{{
        row.birthplace ? row.birthplace : ""
      }}</template>
      <template #created-data="{ row }">{{
        new Date(row.created).toLocaleDateString()
      }}</template>
      <template #username-data="{ row }">{{
        row.username ? row.username.toString().split(" ")[0] : ""
      }}</template>
      <template #editable-data="{ row }">
        <div
          class="text-center me-12"
          :class="row.editable ? 'animate-pulse' : ''"
        >
          <UChip size="2xl" :color="row.editable ? 'red' : 'green'" />
        </div>
      </template>
      <template #caption>
        <caption class="caption-bottom text-left">
          <UButton
            variant="link"
            icon="i-heroicons-arrow-path"
            :label="`Обновлено: ${persons.updated}`"
            @click="refresh"
          />
        </caption>
      </template>
    </UTable>
    <div
      v-if="persons.prev || persons.next"
      class="grid place-items-center py-8"
    >
      <UButtonGroup orientation="horizontal">
        <UButton
          :disabled="!persons.prev"
          label="Назад"
          variant="link"
          icon="i-heroicons-chevron-double-left"
          @click="switchPage(persons.page - 1)"
        />
        <UButton
          :disabled="!persons.next"
          label="Вперед"
          variant="link"
          trailing
          icon="i-heroicons-chevron-double-right"
          @click="switchPage(persons.page + 1)"
        />
      </UButtonGroup>
    </div>
  </LayoutsMenu>
</template>
