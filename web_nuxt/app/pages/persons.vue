<script setup lang="ts">
import type { FetchResponse } from "ofetch";
import type { TableColumn } from "@nuxt/ui";
import type { Candidate, Person, Session } from "@/types";

const { $api } = useNuxtApp();

const toasts = useToasts();

const { data: session } = useNuxtData<Session>("session");

// Объявляем переменные для работы с данными
const modal = ref(false);
const page = ref(1);
const per_page = 10;
const search = ref("");
const updated = ref(Date.now());

// Определяем функцию для получения списка кандидатов из API
const { data, status, refresh } = await useAsyncData(
  "candidates",
  () =>
    $api<Candidate[]>("/routes/candidates", {
      query: {
        page: page.value - 1,
        per_page: per_page,
        search: search.value,
      },
    }),
  {
    watch: [page],
    default: () => [] as Candidate[],
  },
);

const total = computed(() => {
  return data.value[0]?.total ?? 1;
});

watch(data, () => (updated.value = Date.now()));

// Наблюдаем: поиск
watch(refDebounced(search, 1000), () => {
  if (page.value === 1) refresh();
  else page.value = 1;
});

// Определяем обработчики диалогового окна для загрузки JSON
const { open, onChange } = useFileDialog({
  accept: ".json",
  multiple: false,
});

// Фукция загрузки файла JSON
onChange(async (files) => {
  status.value = "pending";
  const str = (await files?.[0]?.text()) as string;
  const response = await $api.raw("/routes/json", {
    method: "POST",
    body: JSON.parse(str),
  });
  proceedSubmit(response);
});

async function personSubmit(form: Person) {
  modal.value = false;
  const response = await $api.raw("/routes/persons", {
    method: "POST",
    body: form,
  });
  proceedSubmit(response);
}

// Обработчик результата загрузки данных
async function proceedSubmit(response: FetchResponse<unknown>) {
  status.value = "success";
  if (response.status === 201) {
    toasts.create("success", "Анкета загружена!");
    const data = await response.json();
    return navigateTo("/profile/" + data.person_id);
  }
  toasts.create();
}

// Определяем массив данных для таблицы кандидатов
const columns: TableColumn<Candidate>[] = [
  { accessorKey: "id", header: "#" },
  {
    accessorKey: "surname",
    header: "Фамилия",
  },
  {
    accessorKey: "firstname",
    header: "Имя",
  },
  {
    accessorKey: "patronymic",
    header: "Отчество",
    cell: ({ row }) => {
      return row.getValue("patronymic") ?? "";
    },
  },
  {
    accessorKey: "birthday",
    header: "Дата рождения",
    cell: ({ row }) => {
      return new Date(row.getValue("birthday")).toLocaleDateString();
    },
  },
  {
    accessorKey: "updated_at",
    header: "Обновлено",
    cell: ({ row }) => {
      return h(resolveComponent("NuxtTime"), {
        datetime: new Date(row.getValue("updated_at")).getTime() - 60000,
        relative: true,
      });
    },
  },
  {
    accessorKey: "username",
    header: "Сотрудник",
    cell: ({ row }) => {
      return row.original.username.split(" ")[0];
    },
  },
];
</script>

<template>
  <UContainer>
    <UPageHeader title="КАНДИДАТЫ" :ui="{ title: 'text-red-800' }">
      <template #links>
        <!-- меню для действий -->
        <UDropdownMenu
          v-if="session?.role === 'user'"
          :items="[
            {
              label: 'Создать анкету',
              icon: 'i-lucide-user-plus',
              onSelect() {
                modal = true;
              },
            },
            {
              label: 'Загрузить json',
              icon: 'i-lucide-upload',
              onSelect() {
                open();
              },
            },
          ]"
          :content="{ align: 'end' }"
        >
          <UButton
            icon="i-lucide-menu"
            variant="ghost"
            title="Действия"
            :loading="status === 'pending'"
          />
        </UDropdownMenu>
        <!-- Модальное окно для добавления анкеты -->
        <UModal
          v-model:open="modal"
          title="Анкета"
          description="Введите анкетные данные кандидата"
        >
          <template #body>
            <FormsResumeForm @update="personSubmit" />
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <!-- Строка поиска -->
    <div class="my-6">
      <UInput
        id="search"
        v-model="search"
        type="search"
        icon="i-lucide-search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />
    </div>

    <!-- Таблица с данными кандидатов -->
    <UTable
      loading-animation="swing"
      empty="Данные не найдены"
      :loading="status === 'pending'"
      :columns="columns"
      :data="data"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="(_, row) => navigateTo(`/profile/${row.original.id}`)"
    >
      <template #loading>
        <UIcon name="i-lucide-refresh-ccw" mode="css" class="animate-spin" />
      </template>
    </UTable>

    <!-- Кнопка обновления и показа времени обновления -->
    <div class="my-2">
      <UButton
        variant="ghost"
        icon="i-lucide-refresh-ccw"
        title="Обновить данные"
        :loading="status === 'pending'"
        @click="refresh()"
      >
        Обновлено:
        <NuxtTime :datetime="updated" relative />
      </UButton>
    </div>

    <!-- Пагинация -->
    <div class="flex justify-center border-t border-default space-x-2 py-4">
      <UPagination
        v-model:page="page"
        :items-per-page="per_page"
        :total="total"
        :sibling-count="-1"
        @update:page="(p) => (page = p)"
      />
    </div>
  </UContainer>
</template>
