<script setup lang="ts">
import type { Persons } from "@/types";
import { watchDebounced, useFileDialog } from "@vueuse/core";
import type { TableColumn } from "@nuxt/ui";

preloadRouteComponents("/profile/[id]");

const UIcon = resolveComponent("UIcon");

const toast = useToast();

const search = ref("");
const page = ref(1);
const pagination = ref(10);
const editable = ref(false);
const hasNext = ref(false);
const upload = ref(false);
const modal = ref(false);
const updated = ref("Данные обновляются...");
const candidates = ref([] as Persons[]);

const { refresh, status } = await useLazyAsyncData(
  "candidates",
  async () => {
    const { results, has_next } = (await useFetchAuth(
      "/route/index/" + page.value,
      {
        params: {
          search: search.value,
          editable: editable.value,
          pagination: pagination.value,
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
    watch: [page, pagination, editable],
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
        title: "Успех",
        description: "Анкета загружена.",
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
        title: "Ошибка",
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
  const { person_id, exists } = (await useFetchAuth("/route/json", {
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
  const { person_id, exists } = (await useFetchAuth("/route/resume", {
    method: "POST",
    body: form,
  })) as {
    person_id: string;
    exists: boolean;
  };
  upload.value = false;
  sendMessage(person_id, exists);
}

const columns: TableColumn<Persons>[] = [
  { accessorKey: "id", header: "#" },
  { accessorKey: "region", header: "Регион" },
  {
    accessorKey: "surname",
    header: "Фамилия Имя Отчество",
    cell: ({ row }) => {
      return `${row.original.surname} ${row.original.firstname} ${
        row.original.patronymic ? row.original.patronymic : ""
      }`;
    },
  },
  {
    accessorKey: "birthday",
    header: "Дата рождения",
    cell: ({ row }) => {
      return new Date(row.original.birthday).toLocaleDateString("ru-RU");
    },
  },
  {
    accessorKey: "editable",
    header: "Статус",
    cell: ({ row }) => {
      return h(UIcon, {
        name: row.original.editable
          ? "i-heroicons-arrow-path"
          : "i-heroicons-check-circle",

        class: row.original.editable
          ? "text-start w-4 h-4 animate-spin text-red-800"
          : "text-start w-4 h-4 text-blue-800",
      });
    },
  },
  {
    accessorKey: "created",
    header: "Обновлено",
    cell: ({ row }) => {
      return new Date(row.original.created).toLocaleDateString("ru-RU");
    },
  },
  {
    accessorKey: "username",
    header: "Сотрудник",
    cell: ({ row }) => {
      return row.original.username
        ? row.original.username.toString().split(" ")[0]
        : "";
    },
  },
];
</script>

<template>
  <div class="mb-6">
    <div class="flex items-center justify-between mb-3">
      <div class="py-1">
        <h3 class="text-2xl text-red-800 font-bold">КАНДИДАТЫ</h3>
      </div>
      <div v-if="stateUser.role == 'user'" class="flex items-center space-x-4">
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
              <FormsResumeForm @cancel="modal = false" @update="submitResume" />
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

    <div class="my-6">
      <UInput
        id="search"
        v-model="search"
        :loading="status == 'pending'"
        type="search"
        icon="i-heroicons-magnifying-glass"
        placeholder="поиск по фамилии, имени, отчеству"
      />
    </div>

    <UTable
      :loading="status == 'pending' || upload"
      loading-animation="carousel"
      empty="Данные не найдены"
      :columns="columns"
      :data="candidates"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="navigateTo(`/profile/${$event.original.id}`)"
    />

    <div class="flex items-center justify-between space-x-4 my-2">
      <UTooltip text="Обновить данные">
        <UButton
          variant="ghost"
          icon="i-heroicons-arrow-path"
          :label="`Обновлено в: ${updated}`"
          :loading="status == 'pending' || upload"
          @click="refresh()"
        />
      </UTooltip>
      <div class="flex items-center space-x-2">
        <div class="text-sm text-blue-600">
          {{ editable ? "Показать все" : "Показать редактируемые" }}
        </div>
        <USwitch v-model="editable" size="sm" />
      </div>
    </div>

    <div v-if="page > 1 || hasNext" class="flex justify-center space-x-2 my-2">
      <UTooltip text="Предыдущая страница">
        <UButton
          icon="i-heroicons-arrow-small-left-20-solid"
          :disabled="page < 2"
          class="me-2 rounded-full"
          @click="page--"
        />
      </UTooltip>
      <USelect
        v-model="pagination"
        :items="[10, 20, 30, 50]"
        :loading="status == 'pending'"
        :disabled="!hasNext"
        variant="soft"
      />
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
