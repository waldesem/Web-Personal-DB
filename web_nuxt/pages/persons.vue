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

function sendMessage(person_id: string, exists: boolean) {
  if (person_id) {
    if (exists) {
      toast.add({
        icon: "i-heroicons-exclamation-triangle",
        title: "Внимание",
        description: "Кандидат ранее уже был загружен",
        color: "secondary",
      });
    } else {
      toast.add({
        icon: "i-heroicons-information-circle",
        title: "Внимание",
        description: "Анкета успешно загружена.",
        color: "success",
      });
    }
    navigateTo("/profile/" + person_id);
  } else {
    if (exists) {
      toast.add({
        icon: "i-heroicons-information-circle",
        title: "Внимание",
        description:
          "Анкета находится в другом регионе или назначена иному пользователю",
        color: "warning",
      });
    } else {
      toast.add({
        icon: "i-heroicons-information-circle",
        title: "Внимание",
        description: "Невозможно выполнить действие",
        color: "error",
      });
    }
  }
}

onChange(async (files) => {
  if (!files) return;
  upload.value = true;
  const formData = new FormData();
  formData.append("file", files[0]);
  const { person_id, exists } = (await authFetch("/route/anketa/json", {
    method: "POST",
    body: formData,
  })) as {
    person_id: string;
    exists: boolean;
  };
  reset();
  upload.value = false;
  sendMessage(person_id, exists);
});

onCancel(() => {
  reset();
});

async function submitResume(form: Persons): Promise<void> {
  upload.value = true;
  modal.value = false;
  const { person_id, exists } = (await authFetch("/route/anketa/resume", {
    method: "POST",
    body: form,
  })) as {
    person_id: string;
    exists: boolean;
  };
  upload.value = false;
  sendMessage(person_id, exists);
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
          <UModal
            v-model:open="modal"
            :dismissible="false"
            title="Создание анкеты"
            description="Введите данные анкеты"
          >
            <template #content>
              <UCard class="m-2">
                <FormsResumeForm
                  @cancel="modal = false"
                  @update="submitResume"
                />
              </UCard>
            </template>
          </UModal>
          <UTooltip text="Загрузить json">
            <UButton
              :loading="status == 'pending' || upload"
              icon="i-heroicons-cloud-arrow-up"
              size="xl"
              variant="ghost"
              @click="open()"
            />
          </UTooltip>
        </div>
      </div>
    </div>
    <div class="my-6">
      <UInput
        id="search"
        v-model="search"
        :loading="status == 'pending'"
        size="lg"
        type="search"
        icon="i-heroicons-magnifying-glass"
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
        { accessorKey: 'id', header: '#' },
        { accessorKey: 'region', header: 'Регион' },
        { accessorKey: 'surname', header: 'Фамилия Имя Отчество' },
        { accessorKey: 'birthday', header: 'Дата рождения' },
        { accessorKey: 'editable', header: 'Статус' },
        { accessorKey: 'created', header: 'Обновлено' },
        { accessorKey: 'username', header: 'Сотрудник' },
      ]"
      :data="candidates"
      @select="navigateTo(`/profile/${$event.original.id}`)"
    >
      <template #id-cell="{ row }">{{ row.original.id }}</template>
      <template #region-cell="{ row }">{{ row.original.region }}</template>
      <template #surname-cell="{ row }">
        {{
          `${row.original.surname} ${row.original.firstname} ${
            row.original.patronymic ? row.original.patronymic : ""
          }`
        }}
      </template>
      <template #birthday-cell="{ row }">{{
        new Date(row.original.birthday).toLocaleDateString("ru-RU")
      }}</template>
      <template #editable-cell="{ row }">
        <UTooltip
          :text="
            row.original.editable ? 'Анкета редактируется' : 'Анкета обновлена'
          "
        >
          <UIcon
            :name="
              row.original.editable
                ? 'i-heroicons-arrow-path'
                : 'i-heroicons-check-circle'
            "
            class="text-start w-4 h-4"
            :class="{ 'animate-spin text-red-800': row.original.editable }"
          />
        </UTooltip>
      </template>
      <template #created-cell="{ row }">{{
        new Date(row.original.created).toLocaleDateString("ru-RU")
      }}</template>
      <template #username-cell="{ row }">{{
        row.original.username
          ? row.original.username.toString().split(" ")[0]
          : ""
      }}</template>
    </UTable>

    <div class="flex items-center justify-between space-x-4">
      <UButton
        variant="ghost"
        icon="i-heroicons-arrow-path"
        :label="`Обновлено в: ${updated}`"
        :loading="status == 'pending' || upload"
        @click="refresh()"
      />
      <div class="flex items-center space-x-2">
        <div class="text-sm text-blue-600">Показать редактируемые</div>
        <USwitch v-model="editable" size="sm" />
      </div>
    </div>

    <div v-if="page > 1 || hasNext" class="justify-center flex pt-4">
      <UTooltip text="Предыдущая страница">
        <UButton
          icon="i-heroicons-arrow-small-left-20-solid"
          :disabled="page < 2"
          class="me-2 rounded-full"
          @click="page--"
        />
      </UTooltip>
      <UTooltip text="Следующая страница">
        <UButton
          icon="i-heroicons-arrow-small-right-20-solid"
          :disabled="!hasNext"
          class="ms-2 rounded-full"
          @click="page++"
        />
      </UTooltip>
    </div>
  </div>
</template>
