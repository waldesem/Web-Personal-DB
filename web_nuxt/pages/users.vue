<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { watchDebounced } from "@vueuse/core";
import type { User } from "@/types";

const fetchAuth = useFetchAuth();

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
  const data = (await fetchAuth("/route/users", {
    params: {
      search: search.value,
    },
  })) as User[];
  users.value = data;
});

async function getUser(id: string): Promise<void> {
  user.value = (await fetchAuth("/route/user/" + id)) as User;
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
  { accessorKey: "role", header: "Роль" },
  { accessorKey: "attempt", header: "Попытка" },
  { accessorKey: "blocked", header: "Блок" },
  { accessorKey: "change_pswd", header: "Изм.пароля" },
];
</script>

<template>
  <div class="mb-6">
    <div class="py-1">
      <h3 class="text-2xl text-gray-800 font-bold">ПОЛЬЗОВАТЕЛИ</h3>
    </div>
    <div class="my-6">
      <UInput v-model="search" placeholder="Поиск по имени пользователя" />
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
    <UModal v-model="modalForm">
      <FormsUserForm
        @cancel="modalForm = false"
        @update="
          modalForm = false;
          refresh();
        "
      />
    </UModal>

    <UModal v-model="modalProfile" prevent-close>
      <DivsUserDiv
        :user="user"
        @update="getUser"
        @cancel="
          modalProfile = false;
          user = {} as User;
          refresh();
        "
      />
    </UModal>

    <UTable
      :loading="status === 'pending'"
      :progress="{ color: 'red', animation: 'swing' }"
      :empty-state="{
        icon: 'i-heroicons-circle-stack-20-solid',
        label: 'Пользователи не найдены.',
      }"
      :data="filtredUsers"
      :columns="columns"
      @select="getUser($event.id)"
    >
      <template #id-cell="{ row }">{{ row.id }}</template>
      <template #fullname-cell="{ row }">{{ row.fullname }}</template>
      <template #username-cell="{ row }">{{ row.username }}</template>
      <template #region-cell="{ row }">{{ row.region }}</template>
      <template #role-cell="{ row }">{{ row.role }}</template>
      <template #attempt-cell="{ row }">
        <div class="text-center">
          {{ row.attempt }}
        </div>
      </template>
      <template #blocked-cell="{ row }">
        <div class="text-center">
          <UIcon
            :name="
              row.blocked ? 'i-heroicons-lock-closed' : 'i-heroicons-lock-open'
            "
          />
        </div>
      </template>
      <template #change_pswd-cell="{ row }">
        <div class="text-center">
          <UIcon
            :name="
              row.change_pswd
                ? 'i-heroicons-lock-closed'
                : 'i-heroicons-lock-open'
            "
          />
        </div>
      </template>
    </UTable>
  </div>
</template>
