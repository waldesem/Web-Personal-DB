<script setup lang="ts">
import type { TableColumn } from "@nuxt/ui";
import type { Session, User } from "@/types";

// Объявляем переменные для рендера компонентов
const UIcon = resolveComponent("UIcon");
const UBadge = resolveComponent("UBadge");
const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");

const toasts = useToasts();

const { data: user } = useNuxtData<Session>("session");

// Вызываем плагин для работы с API
const { $api } = useNuxtApp();

// Определяем переменные для работы с данными
const modal = ref(false);
const expanded = ref({ 1: false });
// const globalFilter = ref("");

// Определяем функцию для получения данных из API
const { data, status, refresh } = await useLazyAsyncData<User[]>(
  "users",
  () => $api("/routes/users"),
  { default: () => [] as User[] },
);

// Объявляем функцию для действия с пользователем
async function userAction(item: string, user_id: string) {
  if (!confirm("Подтвердите выполнение действия")) return;
  if (user_id === user.value?.id) return;
  const { message } = await $api<Record<string, string>>(
    "/routes/user/" + user_id,
    {
      method: "POST",
      body: { item: item },
    },
  );
  if (message == "success") {
    toasts.create("success", "Действие успешно выполнено");
  } else {
    toasts.create();
  }
  refresh();
}

// Объявляем функцию для изменения данных таблицы
function getRowItems(user: User) {
  return [
    {
      label: user.deleted ? "Восстановить" : "Удалить",
      onSelect() {
        userAction("delete", user.id);
      },
    },
    {
      label: user.blocked ? "Разблокировать" : "Заблокировать",
      onSelect() {
        userAction("block", user.id);
      },
    },
    {
      label: "Сбросить пароль",
      onSelect() {
        userAction("reset", user.id);
      },
    },
    {
      label: "Изменить роль",
      children: [
        {
          label: "admin",
          onSelect() {
            userAction("admin", user.id);
          },
        },
        {
          label: "api",
          onSelect() {
            userAction("api", user.id);
          },
        },
        {
          label: "user",
          onSelect() {
            userAction("user", user.id);
          },
        },
        {
          label: "guest",
          onSelect() {
            userAction("guest", user.id);
          },
        },
      ],
    },
  ];
}

// Определяем массив данных для таблицы пользователей
const columns: TableColumn<User>[] = [
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
  { accessorKey: "fullname", header: "Пользователь" },
  { accessorKey: "username", header: "Логин" },
  {
    accessorKey: "role",
    header: "Роль",
    cell: ({ row }) => {
      return h(UBadge, {
        color:
          row.original.role === "admin"
            ? "error"
            : row.original.role === "user"
              ? "success"
              : row.original.role === "guest"
                ? "secondary"
                : "neutral",
        label: row.original.role,
      });
    },
  },
  {
    accessorKey: "created_at",
    header: "Создан",
    cell: ({ row }) => {
      return new Date(row.original.created_at).toLocaleDateString();
    },
  },
  {
    accessorKey: "updated_at",
    header: "Обновлен",
    cell: ({ row }) => {
      return new Date(row.original.updated_at).toLocaleDateString();
    },
  },
  { accessorKey: "attempt", header: "Попыток" },
  {
    accessorKey: "blocked",
    header: "Блокир.",
    cell: ({ row }) => {
      return h(UIcon, {
        name: row.original.blocked ? "i-lucide-lock" : "i-lucide-lock-open",
        class: "text-center w-4 h-4",
        title: row.original.blocked ? "Заблокирован" : "Разблокирован",
      });
    },
  },
  {
    accessorKey: "change_pswd",
    header: "Пароль",
    cell: ({ row }) => {
      return h(UIcon, {
        name: row.original.change_pswd
          ? "i-lucide-clock-alert"
          : "i-lucide-clock",
        class: "text-center w-4 h-4",
        title: row.original.change_pswd
          ? "Требуется смена пароля"
          : "Смена пароля не требуется",
      });
    },
  },
  {
    accessorKey: "deleted",
    header: "Удален",
    cell: ({ row }) => {
      return h(UIcon, {
        name: row.original.deleted ? "i-lucide-user-x" : "i-lucide-user-check",
        class: row.original.deleted
          ? "text-center w-4 h-4 text-red-600"
          : "text-center w-4 h-4 text-green-600",
        title: row.original.deleted
          ? "Помечен на удаление"
          : "Пользователь активен",
      });
    },
  },
  {
    id: "actions",
    cell: ({ row }) => {
      return h(
        "div",
        { class: "text-right" },
        h(
          UDropdownMenu,
          {
            content: {
              align: "end",
            },
            items: getRowItems(row.original),
            "aria-label": "Actions dropdown",
          },
          () =>
            h(UButton, {
              icon: "i-lucide-ellipsis-vertical",
              color: "neutral",
              variant: "ghost",
              class: "ml-auto",
            }),
        ),
      );
    },
  },
];
</script>

<template>
  <UContainer>
    <UPageHeader title="ПОЛЬЗОВАТЕЛИ" :ui="{ title: 'text-gray-800' }">
      <template #links>
        <UModal v-model:open="modal" title="Пользователь">
          <UButton
            variant="ghost"
            size="lg"
            icon="i-lucide-user-plus"
            title="Добавить пользователя"
            @click="modal = true"
          />
          <!-- Вставляем форму для добавления пользователя -->
          <template #body>
            <FormsUserForm
              @update="
                modal = false;
                refresh();
              "
            />
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <!-- Строка поиска -->
    <div class="my-6">
      <!-- <UInput
        v-model="globalFilter"
        icon="i-lucide-search"
        placeholder="Поиск пользователей"
        type="search"
      /> -->
    </div>
    <!-- Таблица с данными пользователей -->
    <UTable
      v-model:expanded="expanded"
      sticky
      class="flex-1 max-h-[800px]"
      :data="data"
      :columns="columns"
      :loading="status === 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
    >
      <template #expanded="{ row }">
        <!-- Выводим подробную информацию о пользователе -->
        <pre class="text-break">{{ row.original }}</pre>
      </template>
    </UTable>
  </UContainer>
</template>
