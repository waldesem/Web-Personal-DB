<script setup lang="ts">
import { debounce } from "@/utils/utilities";
import { server, stateClassify } from "@/state/state";
import type { User } from "@/utils/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const classifyState = stateClassify();

const dataUsers = ref({
  search: "",
  userId: "",
  region: "",
  role: "",
  users: [] as User[],
  form: {} as User,
  collapsed: false,
  viewDeleted: false,
});

/**
 * Filters the list of users based on the current search query.
 *
 * @return {User[]} An array of user objects
 */
const users = computed(() => {
  return dataUsers.value.users.filter(
    (user: User) => user.deleted == dataUsers.value.viewDeleted
  );
});

/**
 * Fetches a list of users from the server based on the current search query.
 *
 * @return {User[]} An array of user objects
 */
async function getUsers() {
  const fetchAuth = useFetchAuth();
  dataUsers.value.users = (await fetchAuth(`${server}/users`, {
    params: {
      search: dataUsers.value.search,
    },
  })) as unknown as User[];
}

/**
 * Performs an action on a user, such as blocking or deleting them.
 * 
 * @param {string} item The action to perform
 * @param {string} id The ID of the user to perform the action on
 * @returns {Promise<void>}
 */
async function userAction(
  item: string,
  id: string = dataUsers.value.userId
): Promise<void> {
  if (!confirm("Подтвердите действие!")) {
    return;
  }
  const fetchAuth = useFetchAuth();
  await fetchAuth(`${server}/users/${id}`, {
    params: {
      item: item,
    },
  });
  Object.assign(dataUsers.value, {
    userId: "",
    region: "",
    role: "",
  });
  await getUsers();
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: "Действие успешно выполнено",
    color: "green",
  });
}

/**
 * Submits a new user to the server.
 * @returns {Promise<void>}
 */
async function submitUser(): Promise<void> {
  const fetchAuth = useFetchAuth();
  await fetchAuth(`${server}/users`, {
    method: "POST",
    body: dataUsers.value.form,
  });
  dataUsers.value.collapsed = false;
  await getUsers();
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: "Пользователь успешно добавлен",
    color: "green",
  });
}

/**
 * Searches for users based on the current search query.
 */
const searchUser = debounce(async () => {
  await getUsers();
}, 500);

/**
 * The dropdown menu items for a user action.
 */
const items = [
  [
    {
      label: "Сбросить пароль",
      click: () => userAction("drop"),
    },
  ],
  [
    {
      label: "Заблокировать/разблокировать",
      click: () => userAction("block"),
    },
  ],
  [
    {
      label: "Удалить/восстановить",
      click: () => userAction("delete"),
    },
  ],
];

await getUsers();
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv 
      :div="'py-1'" 
      :cls="'text-2xl text-gray-500'"
      :header="'ПОЛЬЗОВАТЕЛИ'"
    />
    <div class="my-6">
      <UInput
        v-model="dataUsers.search"
        size="lg"
        placeholder="Поиск по имени пользователя"
        @input.prevent="searchUser"
      />
    </div>
    <div class="flex items-center justify-between mb-4">
      <UToggle v-model="dataUsers.viewDeleted" :label="'Показать удаленные'" />
      <UButton
        variant="link"
        label="Добавить пользователя"
        @click="dataUsers.collapsed = !dataUsers.collapsed"
      />
    </div>
    <Transition name="slide-fade">
      <UForm
        v-if="dataUsers.collapsed"
        :state="dataUsers.form"
        @submit.prevent="submitUser"
      >
        <div class="flex grid grid-cols-5 gap-3 border rounded p-3">
          <div class="col-span-2">
            <UFormGroup required class="mb-3">
              <UInput
                v-model="dataUsers.form['fullname']"
                placeholder="Имя пользователя"
                size="lg"
              />
            </UFormGroup>
          </div>
          <div class="col-span-2">
            <UFormGroup required class="mb-3">
              <UInput
                v-model="dataUsers.form['username']"
                placeholder="Логин"
                size="lg"
              />
            </UFormGroup>
          </div>
          <div class="col-span-1">
            <UButton
              block
              variant="outline"
              color="gray"
              label="Создать"
              type="submit"
              size="lg"
            />
          </div>
        </div>
      </UForm>
    </Transition>
    <UTable
      :columns="[
        { key: 'id', label: '#' },
        { key: 'fullname', label: 'Пользователь' },
        { key: 'username', label: 'Логин' },
        { key: 'region', label: 'Регион' },
        { key: 'role', label: 'Роль' },
        { key: 'created', label: 'Создан' },
        { key: 'attempt', label: 'Попытки' },
        { key: 'blocked', label: 'Блокировка' },
        { key: 'pswd_create', label: 'Обновлено' },
        { key: 'change_pswd', label: 'Изменение' },
      ]"
      :rows="users"
    >
      <template #id-data="{ row }">{{ row.id }}</template>
      <template #fullname-data="{ row }">{{ row.fullname }}</template>
      <template #username-data="{ row }">
        <UDropdown :items="items">
          <UButton
            variant="link"
            :label="row.username"
            @click="dataUsers.userId = row.id"
          />
        </UDropdown>
      </template>
      <template #region-data="{ row }">
        <USelect
          v-model="dataUsers.region"
          :placeholder="row.region"
          :options="Object.values(classifyState.classes.value.regions)"
          @change="userAction(dataUsers.region, row.id)"
        />
      </template>
      <template #role-data="{ row }">
        <USelect
          v-model="dataUsers.role"
          :placeholder="row.role"
          :options="Object.values(classifyState.classes.value.roles)"
          @change="userAction(dataUsers.role, row.id)"
        />
      </template>
      <template #created-data="{ row }">{{
        new Date(row.created).toLocaleDateString()
      }}</template>
      <template #blocked-data="{ row }">
        <UChip size="2xl" :color="row.blocked ? 'red' : 'green'" />
      </template>
      <template #pswd_create-data="{ row }">{{
        new Date(row.pswd_create).toLocaleDateString()
      }}</template>
      <template #change_pswd-data="{ row }">
        <UChip size="2xl" :color="row.change_pswd ? 'red' : 'green'" />
      </template>
    </UTable>
  </LayoutsMenu>
</template>
