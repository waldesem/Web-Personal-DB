<script setup lang="ts">
import type { TableColumn } from "@nuxt/ui";
import { watchDebounced } from "@vueuse/core";
import type { User } from "@/types";

const UIcon = resolveComponent("UIcon");
const UBadge = resolveComponent("UBadge");

const search = ref("");
const users = ref([] as User[]);
const user = ref({} as User);
const modalForm = ref(false);
const modalProfile = ref(false);
const viewDeleted = ref(false);

/**
 * Filters the list of users based on the current search query.
 *
 * @return {User[]} An array of user objects
 */
const filtredUsers = computed(() => {
  return users.value.filter((user: User) => user.deleted == viewDeleted.value);
});

const { refresh, status } = await useLazyAsyncData("users", async () => {
  const data = (await useFetchAuth("/route/users", {
    params: {
      search: search.value,
    },
  })) as User[];
  users.value = data;
});

async function getUser(id: string): Promise<void> {
  user.value = (await useFetchAuth("/route/user/" + id)) as User;
  modalProfile.value = true;
}

watchDebounced(
  search,
  () => {
    refresh();
  },
  {
    debounce: 1000,
    maxWait: 2000,
  }
);

const columns: TableColumn<User>[] = [
  { accessorKey: "id", header: "#" },
  { accessorKey: "fullname", header: "Пользователь" },
  { accessorKey: "username", header: "Логин" },
  { accessorKey: "email", header: "Email" },
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
  { accessorKey: "attempt", header: "Попытка" },
  {
    accessorKey: "blocked",
    header: "Блок",
    cell: ({ row }) => {
      return h(UIcon, {
        name: row.original.blocked
          ? "i-heroicons-lock-closed-solid"
          : "i-heroicons-lock-open",
        class: "text-center w-4 h-4",
      });
    },
  },
  {
    accessorKey: "change_pswd",
    header: "Изм.пароля",
    cell: ({ row }) => {
      return h(UIcon, {
        name: row.original.change_pswd
          ? "i-heroicons-clock-solid"
          : "i-heroicons-clock",
        class: "text-center w-4 h-4",
      });
    },
  },
];
</script>

<template>
  <div class="mb-6">
    <div class="py-1">
      <h3 class="text-2xl text-gray-600 font-bold">ПОЛЬЗОВАТЕЛИ</h3>
    </div>
    <div class="my-6">
      <UInput
        v-model="search"
        icon="i-heroicons-magnifying-glass"
        placeholder="Поиск по имени пользователя"
        type="search"
      />
    </div>
    <div class="flex items-center justify-between mb-4">
      <UFormField class="flex items-center space-x-4 mb-3" label="Удаленные">
        <USwitch v-model="viewDeleted" />
      </UFormField>
      <UButton
        variant="link"
        label="Добавить пользователя"
        @click="modalForm = true"
      />
    </div>
    <UModal
      v-model:open="modalForm"
      :dismissible="false"
      title="Добавление пользователя"
      description="Введите данные пользователя"
    >
      <template #content>
        <FormsUserForm
          @cancel="modalForm = false"
          @update="
            modalForm = false;
            refresh();
          "
        />
      </template>
    </UModal>

    <UModal
      v-model:open="modalProfile"
      :dismissible="false"
      title="Профиль"
      description="Данные профиля пользователя"
    >
      <template #content>
        <DivsUserDiv
          :user="user"
          @update="getUser"
          @cancel="
            modalProfile = false;
            user = {} as User;
            refresh();
          "
      /></template>
    </UModal>

    <UTable
      :loading="status === 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
      :data="filtredUsers"
      :columns="columns"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="getUser($event.original.id)"
    />
  </div>
</template>
