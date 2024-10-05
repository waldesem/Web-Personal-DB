<script setup lang="ts">
import type { User } from "@/types/interfaces";
import { watchDebounced } from "@vueuse/core";

const toast = useToast();

const fetchAuth = useFetchAuth();

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

 const { refresh, status } = await useLazyAsyncData("users", async () => {
  dataUsers.value.users = await fetchAuth("/api/users", {
      params: {
        search: dataUsers.value.search,
      },
    }) as User[];
  }
);

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
  await fetchAuth("/api/users/" + id, {
    params: {
      item: item,
    },
  });
  Object.assign(dataUsers.value, {
    userId: "",
    region: "",
    role: "",
  });
  await refresh();
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
  await fetchAuth("/api/users", {
    method: "POST",
    body: dataUsers.value.form,
  });
  dataUsers.value.collapsed = false;
  Object.assign(dataUsers.value.form, {
    fullname: "",
    username: "",
  });
  await refresh();
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: "Пользователь успешно добавлен",
    color: "green",
  });
}

const validate = (state: User) => {
  const errors = [];
  if (state.fullname && !state.fullname.match(/^[а-яёЁА-Я-\s]+$/)) {
    errors.push({
      path: "fullname",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (state.username && !state.username.match(/^[a-zA-Z_\s]+$/)) {
    errors.push({
      path: "username",
      message:
        "Поле должно содержать только латинские буквы и знаки подчеркивания",
    });
  }
  if (
    state.email &&
    !state.email.match(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/)
  ) {
    errors.push({
      path: "email",
      message: "Поле должно содержать корректную почту",
    });
  }
  return errors;
};

watchDebounced(
  () => dataUsers.value.search,
  () => {
    refresh();
  },
  {
    debounce: 500,
    maxWait: 1000,
  }
);

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
</script>

<template>
  <div>
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
        :validate="validate"
        @submit.prevent="submitUser"
      >
        <div class="flex grid grid-cols-7 gap-3 border rounded p-3">
          <div class="col-span-2">
            <UFormGroup required class="mb-3" name="fullname">
              <UInput
                v-model="dataUsers.form['fullname']"
                placeholder="Имя пользователя"
              />
            </UFormGroup>
          </div>
          <div class="col-span-2">
            <UFormGroup required class="mb-3" name="username">
              <UInput
                v-model="dataUsers.form['username']"
                placeholder="Логин"
              />
            </UFormGroup>
          </div>
          <div class="col-span-2">
            <UFormGroup required class="mb-3" name="email">
              <UInput v-model="dataUsers.form['email']" placeholder="Email" />
            </UFormGroup>
          </div>
          <div class="col-span-1">
            <UButton
              block
              variant="outline"
              color="gray"
              label="Создать"
              type="submit"
            />
          </div>
        </div>
      </UForm>
    </Transition>
    <UTable
      :loading="status === 'pending'"
      :progress="{ color: 'red', animation: 'swing' }"
      :empty-state="{
        icon: 'i-heroicons-circle-stack-20-solid',
        label: 'Пользователи не найдены.',
      }"
      :columns="[
        { key: 'id', label: '#' },
        { key: 'fullname', label: 'Пользователь' },
        { key: 'username', label: 'Логин' },
        { key: 'email', label: 'Email' },
        { key: 'region', label: 'Регион' },
        { key: 'role', label: 'Роль' },
        { key: 'created', label: 'Создан' },
        { key: 'attempt', label: 'Попытка' },
        { key: 'blocked', label: 'Блок' },
        { key: 'pswd_create', label: 'Обновлен' },
        { key: 'change_pswd', label: 'Изм.пароля' },
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
          :options="[
            'Главный офис',
            'РЦ Юг',
            'РЦ Запад',
            'РЦ Урал',
            'РЦ Восток',
          ]"
          @change="userAction(dataUsers.region, row.id)"
        />
      </template>
      <template #role-data="{ row }">
        <USelect
          v-model="dataUsers.role"
          :placeholder="row.role"
          :options="['admin', 'user', 'guest']"
          @change="userAction(dataUsers.role, row.id)"
        />
      </template>
      <template #created-data="{ row }">{{
        new Date(row.created).toLocaleDateString()
      }}</template>
      <template #attempt-data="{ row }">
        <div class="text-center">
          {{ row.attempt }}
        </div>
      </template>
      <template #blocked-data="{ row }">
        <div class="text-center">
          <UChip size="2xl" :color="row.blocked ? 'red' : 'green'" />
        </div>
      </template>
      <template #pswd_create-data="{ row }">{{
        new Date(row.pswd_create).toLocaleDateString()
      }}</template>
      <template #change_pswd-data="{ row }">
        <div class="text-center">
          <UChip size="2xl" :color="row.change_pswd ? 'red' : 'green'" />
        </div>
      </template>
    </UTable>
  </div>
</template>
