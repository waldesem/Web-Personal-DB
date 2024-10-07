<script setup lang="ts">
import type { Persons } from "@/types/interfaces";
import { watchDebounced, useFileDialog, useDateFormat } from "@vueuse/core";

preloadRouteComponents("/profile/[id]");

const authFetch = useFetchAuth();
const userState = useUserState();
const toast = useToast();

const persons = ref({
  candidates: [] as Persons[],
  page: 1,
  prev: false,
  next: false,
  search: "",
  upload: false,
  updated: useDateFormat(useNow(), "DD.MM.YYYY в HH:mm").value,
});

const { refresh, status } = await useLazyAsyncData("candidates", async () => {
  const response = await authFetch("/api/index/" + persons.value.page, {
    params: {
      search: persons.value.search,
    },
  });

  [persons.value.candidates, persons.value.next, persons.value.prev] =
    response as [Persons[], boolean, boolean];

  persons.value.updated = useDateFormat(useNow(), "DD.MM.YYYY в HH:mm").value;
});

watchDebounced(
  () => persons.value.search,
  () => {
    refresh();
  },
  {
    debounce: 500,
    maxWait: 1000,
  }
);

watch(
  () => persons.value.page,
  () => {
    refresh();
  }
);

const { open, reset, onCancel, onChange } = useFileDialog({
  accept: "*.json",
  multiple: false,
});

onChange(async (files) => {
  if (!files) return;
  const formData = new FormData();
  formData.append("file", files[0]);
  const { person_id } = (await authFetch("/api/json", {
    method: "POST",
    body: formData,
  })) as Record<string, string>;
  if (!person_id) return;
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: "Файл успешно загружен",
    color: "green",
  });
  persons.value.upload = false;
  await refresh();
  return navigateTo("/profile/" + person_id);
});

onCancel(() => {
  reset();
});
</script>

<template>
  <div>
    <div v-if="userState.role == 'user'" class="relative">
      <div
        class="absolute inset-y-0 right-0"
        :class="{ 'animate-pulse': status == 'pending' || persons.upload }"
      >
        <UButton
          icon="i-heroicons-cloud-arrow-up"
          size="xl"
          title="Загрузить json файл"
          variant="ghost"
          class="w-8 h-8"
          @click="open"
        />
      </div>
    </div>

    <ElementsHeaderDiv :header="'КАНДИДАТЫ'" />
    <div class="my-6">
      <UInput
        v-model="persons.search"
        placeholder="поиск по фамилии, имени, отчеству"
        size="lg"
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

    <div v-if="persons.prev || persons.next" class="justify-center flex py-6">
      <UTooltip text="Предыдущая страница">
        <UButton
          icon="i-heroicons-arrow-small-left-20-solid"
          :disabled="!persons.prev"
          :ui="{ rounded: 'rounded-full' }"
          class="me-2"
          @click="persons.page--"
        />
      </UTooltip>
      <UTooltip text="Следующая страница">
        <UButton
          icon="i-heroicons-arrow-small-right-20-solid"
          :disabled="!persons.next"
          :ui="{ rounded: 'rounded-full' }"
          class="ms-2"
          @click="persons.page++"
        />
      </UTooltip>
    </div>
  </div>
</template>
