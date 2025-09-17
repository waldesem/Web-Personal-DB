<script setup lang="ts">
import { refDebounced, useFileDialog } from "@vueuse/core";
import type { TableColumn } from "@nuxt/ui";
import type { Candidate } from "@/types";

// Прелоадим компонент для загрузки анкеты
await preloadRouteComponents("/profile/[id]");

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Объявляем переменные рендера компонентов
const NuxtTime = resolveComponent("NuxtTime");
const UButton = resolveComponent("UButton");
const UIcon = resolveComponent("UIcon");

// Объявляем переменную для получения данных пользователя
const userState = useStateUser();

// Объявляем переменные для работы с данными
const expanded = ref({ 1: false }); // Состояние раскрытия строк таблицы
const modal = ref(false); // Состояние модального окна
const page = ref(1); // Страница таблицы
const per_page = 10; // Количество строк в таблице
const search = ref(""); // Поисковый запрос
const updated = ref(Date.now()); // Дата обновления данных

// Определяем функцию для получения списка кандидатов из API
const { data, status, refresh } = useLazyAsyncData(
  async () => {
    const response = await $api("/routes/candidates", {
      query: {
        page: page.value,
        per_page: per_page,
        search: search.value,
      },
    });
    updated.value = Date.now();
    return response as Candidate[];
  },
  // Наблюдаем: активность пользователя, переключение страницы, изменение строки поиска.
  { watch: [page, refDebounced(search, 1000)] }
);
// Определяем обработчики диалогового окна для загрузки JSON
const { open, onChange } = useFileDialog({
  accept: ".json",
  multiple: false,
});

// Фукция загрузки файла JSON
onChange(async (files) => {
  if (!files?.[0]?.name.endsWith(".json")) {
    useToasts();
    return;
  }
  status.value = "pending";
  const { person_id, exists } = await $api<{
    person_id: string;
    exists: boolean;
  }>("/routes/json", {
    method: "POST",
    body: files[0],
  });
  proceedResult(person_id, exists);
});

// Определяем функцию для обработки события обновления данных через форму
function handleEmit(person_id: string, exists: boolean) {
  modal.value = false;
  proceedResult(person_id, exists);
}

// Обработчик результата загрузки данных
function proceedResult(person_id: string, exists: boolean) {
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
  // Раскрытие строк таблицы
  {
    id: "expand",
    cell: ({ row }) =>
      h(UButton, {
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
  // ID кандидата
  { accessorKey: "id", header: "#" },
  // Имя кандидата
  {
    accessorKey: "fullname",
    header: "Фамилия Имя Отчество",
    cell: ({ row }) => {
      return `${row.original.surname} ${row.original.firstname} ${
        row.original.patronymic ?? ""
      }`;
    },
  },
  // Дата рождения
  {
    accessorKey: "birthday",
    header: "Дата рождения",
    cell: ({ row }) => {
      return h(NuxtTime, {
        datetime: row.getValue("birthday"),
      });
    },
  },
  // Статус кандидата
  {
    accessorKey: "editable",
    header: "Статус",
    cell: ({ row }) => {
      return h(UIcon, {
        name: !row.getValue("editable")
          ? "i-lucide-circle-check"
          : "i-lucide-triangle-alert",

        class: !row.getValue("editable")
          ? "text-start w-5 h-5 text-blue-600"
          : "text-start w-5 h-5 text-red-600",
        title: !row.getValue("editable")
          ? "Анкета доступна для редактирования"
          : "Анкета находится в режиме редактирования",
      });
    },
  },
  // Обновлено
  {
    accessorKey: "created",
    header: "Обновлено",
    cell: ({ row }) => {
      return h(NuxtTime, {
        datetime: row.getValue("created"),
        relative: true,
      });
    },
  },
  // Сотрудник
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
</script>

<template>
  <div class="py-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-2xl text-red-800 font-bold">КАНДИДАТЫ</h3>
      <!-- Выпадающее меню для действий -->
      <div v-if="userState.role == 'user' && status != 'pending'">
        <ElementsDivMenu
          :label-update="'Создать анкету'"
          :label-refresh="'Загрузить json'"
          :icon-update="'i-lucide-user-plus'"
          :icon-refresh="'i-lucide-upload'"
          @update="modal = true"
          @refresh="open()"
        />

        <!-- Модальное окно для добавления анкеты -->
        <UModal
          v-model:open="modal"
          title="Добавить анкету"
          description="Введите анкетные данные кандидата"
        >
          <!-- Вставляем форму для добавления анкеты -->
          <template #body>
            <LazyFormsResumeForm @update="handleEmit" />
          </template>
        </UModal>
      </div>
      <UIcon 
        v-if="status == 'pending'" 
        name="i-lucide-refresh-ccw" 
        size="24" mode="css" 
        class="animate-spin" 
      />
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
      :loading-color="'neutral'"
      loading-animation="swing"
      empty="Данные не найдены"
      :columns="columns"
      :data="data"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="navigateTo(`/profile/${$event.original.id}`)"
    >
      <!-- Выводим подробную информацию о кандидате -->
      <template #expanded="{ row }">
        <UCard><ItemsPersonItem :item="row.original" /></UCard>
      </template>
      <template #loading>
        <UIcon name="i-lucide-refresh-ccw" size="24" mode="css" class="animate-spin" />
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
