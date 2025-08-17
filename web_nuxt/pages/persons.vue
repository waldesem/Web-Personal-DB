<script setup lang="ts">
import { useFileDialog, watchDebounced } from "@vueuse/core";
import type { DropdownMenuItem, TableColumn } from "@nuxt/ui";
import type { Candidate } from "@/types";

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Прелоадим компонент для загрузки анкеты
await preloadRouteComponents("/profile/[id]");

// Объявляем переменные рендера компонентов
const NuxtTime = resolveComponent("NuxtTime");
const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");
const UIcon = resolveComponent("UIcon");

// Объявляем переменную для получения данных пользователя
const userState = useStateUser();

// Объявляем переменные для работы с данными
const data = shallowRef<Candidate[]>([]);
const expanded = ref({ 1: false });
const modal = ref(false);
const page = ref(1);
const per_page = 10;
const search = ref("");
const updated = ref(Date.now());

// Определяем функцию для получения списка кандидатов из API
const { status, refresh } = await useLazyAsyncData(
  async () => {
    data.value = await $api("/route/index", {
      query: {
        page: page.value,
        per_page: per_page,
        search: search.value,
      },
    });
    updated.value = Date.now();
  },
  { watch: [page] }
);

// Определяем наблюдатель за изменением строки поиска
watchDebounced(search, async () => await refresh(), {
  debounce: 1000,
  maxWait: 2000,
});

// Определяем данные для загрузки файла JSON
const { open, onChange, reset } = useFileDialog({
  accept: ".json",
  multiple: false,
});

// Обработчик загрузки файла JSON
onChange(async (files) => {
  if (!files?.length) return;
  status.value = "pending";
  const formData = new FormData();
  formData.append("file", files[0] as File);
  const { person_id, exists } = await $api<{
    person_id: string;
    exists: boolean;
  }>("/route/json", {
    method: "POST",
    body: formData,
  });
  reset();
  proceedResult(person_id, exists);
});

// Определяем функцию для закрытия диалога
function submitResume(person_id: string, exists: boolean) {
  modal.value = false;
  proceedResult(person_id, exists);
}

// Обработчик закрытия диалога
async function proceedResult(person_id: string, exists: boolean) {
  status.value = "success";
  if (person_id) {
    if (exists) {
      useToasts("info", "Кандидат ранее уже был загружен");
    } else {
      useToasts("success", "Анкета успешно загружена");
    }
    return navigateTo("/profile/" + person_id);
  } else {
    if (exists) {
      useToasts("info", "Анкета назначена другому пользователю");
    } else {
      useToasts();
    }
  }
}

// Определяем массив данных для таблицы кандидатов
const columns: TableColumn<Candidate>[] = [
  {
    id: "expand",
    cell: ({ row }) =>
      h(UButton, {
        color: "neutral",
        variant: "ghost",
        icon: "i-lucide-chevron-down",
        square: true,
        ui: {
          leadingIcon: [
            "transition-transform",
            row.getIsExpanded() ? "duration-200 rotate-180" : "",
          ],
        },
        onClick: () => row.toggleExpanded(),
      }),
  },
  { accessorKey: "id", header: "#" },
  { accessorKey: "fullname", header: "Фамилия Имя Отчество" },
  {
    accessorKey: "birthday",
    header: "Дата рождения",
    cell: ({ row }) => {
      return h(NuxtTime, {
        datetime: row.original.birthday,
      });
    },
  },
  {
    accessorKey: "editable",
    header: "Статус",
    cell: ({ row }) => {
      return h(UIcon, {
        name: !row.original.editable
          ? "i-lucide-circle-check"
          : "i-lucide-triangle-alert",

        class: !row.original.editable
          ? "text-start w-5 h-5 text-blue-600"
          : "text-start w-5 h-5 text-red-600",
        title: !row.original.editable
          ? "Анкета доступна для редактирования"
          : "Анкета находится в режиме редактирования",
      });
    },
  },
  {
    accessorKey: "created",
    header: "Обновлено",
    cell: ({ row }) => {
      return h(NuxtTime, {
        datetime: row.original.created,
        relative: true,
      });
    },
  },
  {
    accessorKey: "username",
    header: "Сотрудник",
    cell: ({ row }) => {
      try {
        return row.original.username.split(" ")[0];
      } catch {
        return "";
      }
    },
  },
];

// Определяем массив данных для выпадающего меню
const items: DropdownMenuItem[] = [
  {
    label: "Создать анкету",
    icon: "i-lucide-user-plus",
    onSelect() {
      modal.value = true;
    },
  },
  {
    label: "Загрузить json",
    icon: "i-lucide-upload",
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
      <!-- Выпадающее меню для действий -->
      <div v-if="userState.role == 'user'">
        <UDropdownMenu :items="items" :content="{ align: 'end' }">
          <UButton
            :loading="status === 'pending'"
            icon="i-lucide-ellipsis-vertical"
            variant="ghost"
            size="lg"
            title="Выбор действия"
          />
        </UDropdownMenu>

        <!-- Модальное окно для добавления анкеты -->
        <UModal
          v-model:open="modal"
          title="Добавить анкету"
          description="Введите анкетные данные кандидата"
        >
          <!-- Вставляем форму для добавления анкеты -->
          <template #body>
            <LazyFormsResumeForm @update="submitResume" />
          </template>
        </UModal>
      </div>
    </div>

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
      v-model:expanded="expanded"
      :loading="status === 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
      :columns="columns"
      :data="data"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="navigateTo(`/profile/${$event.original.id}`)"
    >
      <template #expanded="{ row }">
        <!-- Выводим подробную информацию о кандидате -->
         <ItemsPersonItem :item="row.original" />
      </template>
    </UTable>

    <!-- Кнопка обновления и показа времени обновления -->
    <div class="my-2">
      <UButton
        variant="ghost"
        icon="i-lucide-refresh-ccw"
        :loading="status === 'pending'"
        title="Обновить данные"
        @click="refresh()"
        >Обновлено
        <NuxtTime :datetime="updated" relative />
      </UButton>
    </div>

    <!-- Пагинация -->
    <div class="flex justify-center border-t border-default py-4">
      <UPagination
        v-model:page="page"
        :items-per-page="per_page"
        :total="data?.[0]?.total ?? 1"
        :sibling-count="1"
        @update:page="(p) => (page = p)"
      />
    </div>
  </div>
</template>
