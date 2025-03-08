<script setup lang="ts">
import type { Persons } from "@/types";
import { watchDebounced, useFileDialog } from "@vueuse/core";

preloadRouteComponents("/profile/[id]");

const authFetch = useFetchAuth();

const toast = useToast();

const search = ref("");
const page = ref(1);
const editable = ref(false);
const hasNext = ref(false);
const upload = ref(false);
const modal = ref(false);
const updated = ref("Данные обновляются...");
const candidates = ref([] as Persons[]);

const { refresh, status } = await useLazyAsyncData(
  "candidates",
  async () => {
    const { results, has_next } = (await authFetch(
      "/route/index/" + page.value,
      {
        params: {
          search: search.value,
          editable: editable.value,
        },
      }
    )) as Record<string, unknown> as {
      results: Persons[];
      has_next: boolean;
    };
    candidates.value = results;
    hasNext.value = has_next;
    updated.value = new Date().toLocaleTimeString("ru-RU");
  },
  {
    watch: [page, editable],
  }
);

watchDebounced(
  search,
  () => {
    page.value = 1;
    refresh();
  },
  {
    debounce: 1000,
    maxWait: 2000,
  }
);

const { open, reset, onCancel, onChange } = useFileDialog({
  accept: ".json",
  multiple: false,
});

onChange(async (files) => {
  if (!files) return;
  upload.value = true;
  const formData = new FormData();
  formData.append("file", files[0]);
  const { person_id } = (await authFetch("/route/anketa/json", {
    method: "POST",
    body: formData,
  })) as Record<string, string>;
  reset();
  upload.value = false;
  if (person_id) {
    await navigateTo("/profile/" + person_id);
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description:
        "Файл поврежден или анкета находится в другом регионе или редактируется",
      color: "red",
    });
  }
});

onCancel(() => {
  reset();
});

async function submitResume(form: Persons): Promise<void> {
  upload.value = true;
  modal.value = false;
  const { person_id } = (await authFetch("/route/anketa/resume", {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  upload.value = false;
  if (person_id) {
    navigateTo("/profile/" + person_id);
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Невозможно выполнить действие",
      color: "red",
    });
  }
}
</script>

<template>
  <div class="mb-6">
    <div class="flex items-center justify-between mb-3">
      <div class="py-1">
        <h3 class="text-2xl text-red-800 font-bold">КАНДИДАТЫ</h3>
      </div>
      <div class="flex items-center space-x-4">
        <div v-if="stateUser.role == 'user'">
          <UTooltip text="Создать анкету">
            <UButton
              :loading="status == 'pending' || upload"
              icon="i-heroicons-user-plus"
              size="xl"
              variant="ghost"
              @click="modal = true"
            />
          </UTooltip>
          <UModal v-model="modal" prevent-close>
            <ElementsCardDiv>
              <FormsResumeForm @cancel="modal = false" @update="submitResume" />
            </ElementsCardDiv>
          </UModal>
          <UTooltip text="Загрузить json">
            <UButton
              :loading="status == 'pending' || upload"
              icon="i-heroicons-cloud-arrow-up"
              size="xl"
              variant="ghost"
              @click="open"
            />
          </UTooltip>
        </div>
      </div>
    </div>
    <div class="flex-grow items-center my-6">
      <UInput
        id="search"
        v-model="search"
        size="lg"
        placeholder="поиск по фамилии, имени, отчеству"
      />
    </div>
    <UTable
      :loading="status == 'pending' || upload"
      :loading-state="{
        icon: 'i-heroicons-arrow-path-20-solid',
        label: 'Загрузка...',
      }"
      :empty-state="{
        icon: 'i-heroicons-circle-stack-20-solid',
        label: 'Данные не найдены.',
      }"
      :columns="[
        { key: 'id', label: '#' },
        { key: 'region', label: 'Регион' },
        { key: 'surname', label: 'Фамилия Имя Отчество' },
        { key: 'birthday', label: 'Дата рождения' },
        { key: 'editable', label: 'Статус' },
        { key: 'created', label: 'Обновлено' },
        { key: 'username', label: 'Сотрудник' },
      ]"
      :rows="candidates"
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
        new Date(row.birthday).toLocaleDateString("ru-RU")
      }}</template>
      <template #editable-data="{ row }">
        <UTooltip
          :text="row.editable ? 'Анкета редактируется' : 'Анкета обновлена'"
        >
          <UIcon
            :name="
              row.editable
                ? 'i-heroicons-arrow-path'
                : 'i-heroicons-check-circle'
            "
            class="text-start w-4 h-4"
            :class="{ 'animate-spin text-red-800': row.editable }"
          />
        </UTooltip>
      </template>
      <template #created-data="{ row }">{{
        new Date(row.created).toLocaleDateString("ru-RU")
      }}</template>
      <template #username-data="{ row }">{{
        row.username ? row.username.toString().split(" ")[0] : ""
      }}</template>
      <template #caption>
        <caption class="caption-bottom mt-2">
          <div class="flex items-center justify-between space-x-4">
            <UButton
              variant="ghost"
              icon="i-heroicons-arrow-path"
              :label="`Обновлено в: ${updated}`"
              :loading="status == 'pending' || upload"
              @click="refresh"
            />
            <UCheckbox
              v-model="editable"
              name="editable"
              label="Показать только редактируемые"
            />
          </div>
        </caption>
      </template>
    </UTable>
    <div v-if="page > 1 || hasNext" class="justify-center flex pt-4">
      <UTooltip text="Предыдущая страница">
        <UButton
          icon="i-heroicons-arrow-small-left-20-solid"
          :disabled="page < 2"
          :ui="{ rounded: 'rounded-full' }"
          class="me-2"
          @click="page--"
        />
      </UTooltip>
      <UTooltip text="Следующая страница">
        <UButton
          icon="i-heroicons-arrow-small-right-20-solid"
          :disabled="!hasNext"
          :ui="{ rounded: 'rounded-full' }"
          class="ms-2"
          @click="page++"
        />
      </UTooltip>
    </div>
  </div>
</template>
