<script setup lang="ts">
import type { TableColumn } from "@nuxt/ui";
import type { User } from "@/types";

const UIcon = resolveComponent("UIcon");
const UBadge = resolveComponent("UBadge");
const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");

const { $customFetch } = useNuxtApp();
const userState = useUserState();

const modal = ref(false);
const expanded = ref({ 1: false });
const globalFilter = ref("");

const { data: users, refresh, status } = await useCustomFetch("/route/users", {
  lazy: true,
  server: false,
});

async function userAction(item: string, user_id: string) {
  if (user_id == userState.value.id) {
    makeToast();
    return;
  }
  if (!confirm("Подтвердите выполнение действия")) return;
  const { message } = await $customFetch("/route/user/" + user_id, {
    method: "POST",
    body: { item: item },
  }) as Record<string, string>;
  if (message == "success") {
    makeToast("success", "Действие успешно выполнено");
  } else {
    makeToast();
  }
  refresh();
}

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
      label: "Изменить регион",
      children: [
        {
          label: "Главный офис",
          onSelect() {
            userAction("Главный офис", user.id);
          },
        },
        {
          label: "РЦ Юг",
          onSelect() {
            userAction("РЦ Юг", user.id);
          },
        },
        {
          label: "РЦ Запад",
          onSelect() {
            userAction("РЦ Запад", user.id);
          },
        },
        {
          label: "РЦ Урал",
          onSelect() {
            userAction("РЦ Урал", user.id);
          },
        },
        {
          label: "РЦ Восток",
          onSelect() {
            userAction("РЦ Восток", user.id);
          },
        },
      ],
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
  { accessorKey: "region", header: "Регион" },
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
    accessorKey: "created",
    header: "Создан",
    cell: ({ row }) => {
      return new Date(row.original.created).toLocaleDateString("ru-RU");
    },
  },
  { accessorKey: "attempt", header: "Попыток" },
  {
    accessorKey: "blocked",
    header: "Блокир.",
    cell: ({ row }) => {
      return h(UIcon, {
        name: row.original.blocked
          ? "i-lucide-lock-keyhole"
          : "i-lucide-lock-keyhole-open",
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
            })
        )
      );
    },
  },
];
</script>

<template>
  <div class="py-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-2xl text-gray-500 font-bold">ПОЛЬЗОВАТЕЛИ</h3>
      <UModal
        v-model:open="modal"
        title="Добавить пользователя"
        description="Введите данные пользователя"
      >
        <UButton
          variant="ghost"
          size="lg"
          icon="i-lucide-user-plus"
          title="Добавить пользователя"
          @click="modal = true"
        />
        <template #body>
          <LazyFormsUserForm
            @update="
              modal = false;
              refresh();
            "
          />
        </template>
      </UModal>
    </div>
    <div class="my-6">
      <UInput
        v-model="globalFilter"
        icon="i-lucide-search"
        placeholder="Поиск пользователей"
        type="search"
      />
    </div>
    <UTable
      v-model:expanded="expanded"
      v-model:global-filter="globalFilter"
      sticky
      class="flex-1 max-h-[800px]"
      :data="(users as User[])"
      :columns="columns"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      :loading="status === 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
    >
      <template #expanded="{ row }">
        <pre class="text-break">{{ row.original }}</pre>
      </template>
    </UTable>
  </div>
</template>
