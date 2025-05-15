<script setup lang="ts">
import { watchDebounced, useFileDialog } from "@vueuse/core";
import type { DropdownMenuItem, TableColumn } from "@nuxt/ui";
import type { Persons } from "@/types";

preloadRouteComponents("/profile/[id]");

const UIcon = resolveComponent("UIcon");
const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");

const search = ref("");
const page = ref(1);
const pagination = ref(10);
const editables = ref(false);
const hasNext = ref(false);
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
          editable: editables.value,
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
    watch: [page, pagination, editables],
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

async function createToast(person_id: string, exists: boolean) {
  if (person_id) {
    if (exists) {
      makeToast("info", "Кандидат ранее уже был загружен");
    } else {
      makeToast("success", "Анкета успешно загружена");
    }
    await navigateTo("/profile/" + person_id);
  } else {
    if (exists) {
      makeToast(
        "info",
        "Анкета находится в другом регионе или назначена иному пользователю"
      );
    } else {
      makeToast();
    }
  }
}

onChange(async (files) => {
  if (!files) return;
  status.value = "pending";
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
  status.value = "success";
  createToast(person_id, exists);
});

onCancel(() => {
  reset();
});

async function submitResume(form: Persons): Promise<void> {
  modal.value = false;
  status.value = "pending";
  const { person_id, exists } = (await useFetchAuth("/route/resume", {
    method: "POST",
    body: form,
  })) as {
    person_id: string;
    exists: boolean;
  };
  status.value = "success";
  createToast(person_id, exists);
}

async function openPerson(personId: string) {
  await navigateTo(`/profile/${personId}`);
}

const columns: TableColumn<Persons>[] = [
  { accessorKey: "id", header: "#" },
  { accessorKey: "region", header: "Регион" },
  {
    accessorKey: "surname",
    header: "Фамилия Имя Отчество",
    cell: ({ row }) => {
      return `${row.original.surname} ${row.original.firstname} ${
        row.original.patronymic ?? ""
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
        title: !row.original.editable
          ? "Анкета доступна для редактирования"
          : row.original.user_id == user.value.id
          ? "Анкета назначена текущему пользователю"
          : "Анкета редактируется другим пользователем",
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

const items: DropdownMenuItem[] = [
  {
    label: "Создать анкету",
    icon: "i-heroicons-user-plus",
    onSelect() {
      modal.value = true;
    },
  },
  {
    label: "Загрузить json",
    icon: "i-heroicons-cloud-arrow-up",
    onSelect() {
      open();
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
      <div v-if="user.role == 'user'" class="flex items-center space-x-4">
        <UDropdownMenu :items="items" :content="{ align: 'end' }">
          <UButton
            :loading="status == 'pending'"
            icon="i-heroicons-bars-4"
            variant="ghost"
            title="Выбор действия"
          />
        </UDropdownMenu>
        <UModal
          v-model:open="modal"
          :dismissible="false"
          title="Создание анкеты"
          description="Введите данные анкеты"
        >
          <template #content>
            <div class="m-4">
              <FormsResumeForm @cancel="modal = false" @update="submitResume" />
            </div>
          </template>
        </UModal>
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
      :loading="status == 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
      :columns="columns"
      :data="candidates"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="openPerson($event.original.id)"
    />

    <div class="flex items-center justify-between space-x-4 my-2">
      <UTooltip text="Обновить данные">
        <UButton
          variant="ghost"
          icon="i-heroicons-arrow-path"
          :label="`Обновлено в: ${updated}`"
          :loading="status == 'pending'"
          @click="refresh()"
        />
      </UTooltip>
      <div class="flex items-center space-x-2">
        <div class="text-sm text-blue-600">
          {{ editables ? "Показать все" : "Показать редактируемые" }}
        </div>
        <USwitch v-model="editables" size="sm" />
      </div>
    </div>

    <div v-if="page > 1 || hasNext" class="flex justify-center space-x-2 my-2">
      <UTooltip text="Предыдущая страница">
        <UButton
          icon="i-heroicons-arrow-small-left-20-solid"
          :disabled="page < 2 || status == 'pending'"
          class="me-2 rounded-full"
          @click="page--"
        />
      </UTooltip>
      <USelect
        v-model="pagination"
        :items="[10, 20, 30, 50]"
        :disabled="!hasNext || status == 'pending'"
        variant="soft"
      />
      <UTooltip text="Следующая страница">
        <UButton
          icon="i-heroicons-arrow-small-right-20-solid"
          :disabled="!hasNext || status == 'pending'"
          class="ms-2 rounded-full"
          @click="page++"
        />
      </UTooltip>
    </div>
  </div>
</template>
