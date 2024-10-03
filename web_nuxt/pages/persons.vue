<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

preloadRouteComponents("/profile/[id]");

const authFetch = useFetchAuth();
const userState = stateUser();
const toast = useToast();

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

const { refresh, status } = await useLazyAsyncData("candidates", async () => {
  const response = await authFetch("/api/index/" + persons.value.page, {
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

async function uploadJson(filelist: FileList) {
  if (!filelist) return;
  persons.value.upload = true;
  const formData = new FormData();
  formData.append("file", filelist[0]);
  const { person_id } = (await authFetch("/api/json", {
    method: "POST",
    body: formData,
  })) as Record<string, string>;
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: "Файл успешно загружен",
    color: "green",
  });
  persons.value.upload = false;
  refreshNuxtData("persons");
  return navigateTo("/profile/" + person_id);
}
</script>

<template>
  <div>
    <div v-if="userState.role == 'user'" class="relative">
      <div
        class="absolute inset-y-0 right-0"
        :class="{ 'animate-pulse': status == 'pending' || persons.upload }"
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
            @change="uploadJson($event)"
          />
        </UFormGroup>
      </div>
    </div>
    <ElementsHeaderDiv :header="'КАНДИДАТЫ'" />
    <div class="my-6">
      <UInput
        v-model="persons.search"
        placeholder="поиск по фамилии, имени, отчеству"
        size="lg"
        @input.prevent="searchPerson"
      />
    </div>
    <UTable
      :loading="status == 'pending' || persons.upload"
      :progress="{ color: 'red', animation: 'swing' }"
      :empty-state="{
        icon: 'i-heroicons-circle-stack-20-solid',
        label: 'Данные не найдены.',
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
      @select="navigateTo(`/profile/${$event.id}`)"
    >
      <template #id-data="{ row }">{{ row.id }}</template>
      <template #region-data="{ row }">{{ row.region }}</template>
      <template #surname-data="{ row }">
        {{
          `${row.surname} ${row.firstname} ${
            row.patronymic ? row.patronymic : ""
          }`
        }}
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
          class="text-start"
          :class="row.editable ? 'text-red-600' : 'text-primary'"
        >
          <UIcon
            :name="
              row.editable
                ? 'i-heroicons-arrow-path'
                : 'i-heroicons-check-circle'
            "
            class="w-6 h-6"
            :class="{ ' animate-spin': row.editable }"
          />
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
  </div>
</template>
