<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import { getPaginationRowModel } from "@tanstack/vue-table";
import type { DropdownMenuItem, TableColumn } from "@nuxt/ui";
import type { Persons } from "@/types";

await preloadRouteComponents("/profile/[id]");

const table = useTemplateRef("table");
const UIcon = resolveComponent("UIcon");
const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");

const userState = useUserState();

const modal = ref(false);
const updated = ref("Данные обновляются...");
const candidates = shallowRef([] as Persons[]);
const columnFilters = ref([{ id: "surname", value: "" }]);
const pagination = ref({ pageIndex: 0, pageSize: 10 });

const { refresh, status } = await useLazyAsyncData("candidates", async () => {
  candidates.value = (await fetchAuth("/route/index")) as Persons[];
  updated.value = new Date().toLocaleTimeString("ru-RU");
});

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
    return navigateTo("/profile/" + person_id);
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
  const { person_id, exists } = (await fetchAuth("/route/json", {
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
  const { person_id, exists } = (await fetchAuth("/route/resume", {
    method: "POST",
    body: form,
  })) as {
    person_id: string;
    exists: boolean;
  };
  status.value = "success";
  createToast(person_id, exists);
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
          : row.original.user_id == userState.value.id
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
  <div class="py-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-2xl text-red-800 font-bold">КАНДИДАТЫ</h3>
      <div v-if="userState.role == 'user'">
        <UDropdownMenu :items="items" :content="{ align: 'end' }">
          <UButton
            :loading="status == 'pending'"
            icon="i-heroicons-bars-4"
            variant="ghost"
            size="lg"
            title="Выбор действия"
          />
        </UDropdownMenu>
        <UModal
          v-model:open="modal"
          title="Добавить анкету"
          description="Введите анкетные данные кандидата"
        >
          <template #body>
            <LazyFormsResumeForm @update="submitResume" />
          </template>
        </UModal>
      </div>
    </div>

    <div class="my-6">
      <UInput
        id="search"
        :model-value="(table?.tableApi?.getColumn('surname')?.getFilterValue() as string)"
        type="search"
        icon="i-heroicons-magnifying-glass"
        placeholder="поиск по фамилии, имени, отчеству"
        @update:model-value="
          table?.tableApi?.getColumn('surname')?.setFilterValue($event)
        "
      />
    </div>

    <UTable
      ref="table"
      v-model:column-filters="columnFilters"
      v-model:pagination="pagination"
      :pagination-options="{
        getPaginationRowModel: getPaginationRowModel(),
      }"
      :loading="status == 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
      :columns="columns"
      :data="candidates"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="navigateTo(`/profile/${$event.original.id}`)"
    />

    <div class="my-2">
      <UButton
        variant="ghost"
        icon="i-heroicons-arrow-path"
        :label="`Обновлено в: ${updated}`"
        :loading="status == 'pending'"
        title="Обновить данные"
        @click="refresh()"
      />
    </div>

    <div class="flex justify-center border-t border-default py-4">
      <UPagination
        size="lg"
        :default-page="
          (table?.tableApi?.getState().pagination.pageIndex || 0) + 1
        "
        :items-per-page="table?.tableApi?.getState().pagination.pageSize"
        :total="table?.tableApi?.getFilteredRowModel().rows.length"
        @update:page="(p) => table?.tableApi?.setPageIndex(p - 1)"
      />
    </div>
  </div>
</template>
