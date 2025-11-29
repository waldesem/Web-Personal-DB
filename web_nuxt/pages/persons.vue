<script setup lang="ts">
import { refDebounced, useDateFormat, useFileDialog } from "@vueuse/core";
import type { TableColumn } from "@nuxt/ui";
import type { Candidate } from "@/types";
import { title } from "process";

// Прелоадим компонент
await preloadRouteComponents("/profile/[id]");

const toasts = useToasts();

// Объявляем переменные рендера компонентов
const NuxtTime = resolveComponent("NuxtTime");
const UButton = resolveComponent("UButton");
const UIcon = resolveComponent("UIcon");

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Объявляем переменные для работы с данными
const candidates = ref([] as Candidate[]); // Массив кандидатов
const expanded = ref({ 1: false }); // Состояние раскрытия строк таблицы
const modal = ref(false); // Состояние модального окна
const page = ref(1); // Страница таблицы
const per_page = ref(10); // Количество строк в таблице
const search = ref(""); // Поисковый запрос
const updated = ref(Date.now()); // Дата обновления данных

// Вычисляем количество страниц
const total = computed(() => {
  return candidates.value[0]
    ? Math.ceil(candidates.value[0].total / per_page.value)
    : 1;
});

// Определяем функцию для получения списка кандидатов из API
const { status, refresh } = await useLazyAsyncData(
  "candidates",
  async () => {
    candidates.value = await $api("/routes/candidates", {
      query: {
        page: page.value,
        per_page: per_page.value,
        search: search.value,
      },
    });
    updated.value = Date.now();
  },
  // Наблюдаем: переключение страницы.
  { watch: [page, per_page] }
);

// Наблюдаем: поиск
watch(refDebounced(search, 1000), () => {
  page.value = 1;
  refresh();
});

// Определяем обработчики диалогового окна для загрузки JSON
const { open, onChange } = useFileDialog({
  accept: ".json",
  multiple: false,
});

// Фукция загрузки файла JSON
onChange(async (files) => {
  if (!files?.[0]?.name.endsWith(".json")) {
    toasts.create();
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

// Обработчик результата загрузки данных
async function proceedResult(person_id: string, exists: boolean) {
  modal.value = false;
  status.value = "success";
  if (person_id) {
    if (exists) {
      toasts.create("info", "Кандидат ранее уже был загружен");
    } else {
      toasts.create("success", "Анкета успешно загружена");
    }
    await refresh();
    return navigateTo("/profile/" + person_id);
  } else {
    if (exists) {
      await refresh();
      toasts.create("info", "Анкета назначена другому пользователю");
    } else {
      toasts.create();
    }
    status.value = "success";
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
    cell: ({ row }) =>
      useDateFormat(row.getValue("birthday"), "DD.MM.YYYY").value,
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
          : "Анкета в режиме редактирования",
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
      return row.original.username.split(" ")[0];
    },
  },
];
</script>

<template>
  <UPage>
    <UPageHeader
      title="КАНДИДАТЫ"
      :ui="{
        root: 'relative border-none py-4',
        title: 'text-2xl sm:text-3xl text-red-800',
      }"
    >
      <template #links>
        <!-- меню для действий -->
        <UDropdownMenu
          v-if="userState.role === 'user'"
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
          title="Добавить анкету"
          description="Введите анкетные данные кандидата"
        >
          <template #body>
            <FormsResumeForm
              @update="proceedResult"
              @pending="status === 'pending'"
            />
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
        size="lg"
        icon="i-lucide-search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />
    </div>

    <!-- Таблица с данными кандидатов -->
    <UTable
      v-model:expanded="expanded"
      loading-animation="swing"
      empty="Данные не найдены"
      :loading="status === 'pending'"
      :loading-color="'neutral'"
      :columns="columns"
      :data="candidates"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="(_, row) => navigateTo(`/profile/${row.original.id}`)"
    >
      <!-- Выводим подробную информацию о кандидате -->
      <template #expanded="{ row }">
        <UCard><LazyItemsPersonItem :item="row.original" /></UCard>
      </template>
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
      <UButton
        title="В начало"
        variant="outline"
        icon="i-lucide-chevrons-left"
        :disabled="page === 1"
        @click="page = 1"
      />
      <UButton
        title="Вперед"
        variant="outline"
        icon="i-lucide-chevron-left"
        :disabled="page === 1"
        @click="page--"
      />
      <UInputNumber
        v-model="per_page"
        :min="10"
        :max="100"
        :ui="{ root: 'w-1/8' }"
        title="Количество на странице"
      />
      <UButton
        title="Назад "
        variant="outline"
        trailing-icon="i-lucide-chevron-right"
        :disabled="page === total"
        @click="page++"
      />
      <UButton
        title="В конец"
        variant="outline"
        trailing-icon="i-lucide-chevrons-right"
        :disabled="page === total"
        @click="page = total"
      />
    </div>
  </UPage>
</template>
