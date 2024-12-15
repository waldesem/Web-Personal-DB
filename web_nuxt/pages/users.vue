<script setup lang="ts">
import { watchDebounced } from "@vueuse/core";
import { z } from "zod";
import type { User } from "@/types";

const schema = z.object({
  username: z
    .string({ required_error: "Обязательное поле" })
    .max(255)
    .regex(
      /^[a-zA-Z_\s]+$/,
      "Поле должно содержать только латинские буквы и знаки подчеркивания"
    ),
  fullname: z
    .string({ required_error: "Обязательное поле" })
    .max(255)
    .regex(/^[а-яёЁА-Я-\s]+$/, "Поле должно содержать только русские буквы"),
  email: z
    .string({ required_error: "Обязательное поле" })
    .max(255)
    .regex(
      /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
      "Поле должно содержать корректную почту"
    ),
});

type UserForm = z.infer<typeof schema>;

const toast = useToast();

const fetchAuth = useFetchAuth();

const search = ref("");
const userId = ref("");
const region = ref("");
const role = ref("");
const users = ref([] as User[]);
const form = ref({} as UserForm);
const collapsed = ref(false);
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
  users.value = (await fetchAuth("/route/users", {
    params: {
      search: search.value,
    },
  })) as User[];
});

/**
 * Performs an action on a user, such as blocking or deleting them.
 *
 * @param {string} item The action to perform
 * @param {string} id The ID of the user to perform the action on
 * @returns {Promise<void>}
 */
async function userAction(
  item: string,
  id: string = userId.value
): Promise<void> {
  if (id == stateUser.value.id) {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Невозможно  выполнить действие",
      color: "red",
    });
    return;
  }
  if (!confirm("Подтвердите действие!")) {
    return;
  }
  const { message } = (await fetchAuth("/route/user/" + id, {
    params: {
      item: item,
    },
  })) as Record<string, string>;
  userId.value = "";
  region.value = "";
  role.value = "";
  await refresh();
  if (message != "success") {
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: "Действие успешно выполнено",
      color: "green",
    });
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Действие не было выполнено",
      color: "red",
    });
  }
}

/**
 * Submits a new user to the server.
 * @returns {Promise<void>}
 */
async function submitUser(): Promise<void> {
  const { message } = (await fetchAuth("/route/users", {
    method: "POST",
    body: form.value,
  })) as Record<string, string>;
  collapsed.value = false;
  Object.assign(form.value, {
    fullname: "",
    username: "",
  });
  if (message === "success") {
    await refresh();
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: "Пользователь успешно добавлен",
      color: "green",
    });
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Ошибка данных или пользователь уже существует",
      color: "red",
    });
  }
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
  <div class="mb-6">
    <ElementsHeaderDiv
      :div="'py-1'"
      :cls="'text-2xl text-gray-500'"
      :header="'ПОЛЬЗОВАТЕЛИ'"
    />
    <div class="my-6">
      <UInput
        v-model="search"
        size="lg"
        placeholder="Поиск по имени пользователя"
      />
    </div>
    <div class="flex items-center justify-between mb-4">
      <UToggle v-model="viewDeleted" :label="'Показать удаленные'" />
      <UButton
        variant="link"
        label="Добавить пользователя"
        @click="collapsed = !collapsed"
      />
    </div>
    <Transition name="slide-fade">
      <UForm
        v-if="collapsed"
        :schema="schema"
        :state="form"
        @submit.prevent="submitUser"
      >
        <div class="flex grid grid-cols-7 gap-3 border rounded p-3">
          <div class="col-span-2">
            <UFormGroup class="mb-3" name="fullname" required>
              <UInput
                v-model="form['fullname']"
                placeholder="Имя пользователя"
                required
              />
            </UFormGroup>
          </div>
          <div class="col-span-2">
            <UFormGroup class="mb-3" name="username">
              <UInput v-model="form['username']" placeholder="Логин" required />
            </UFormGroup>
          </div>
          <div class="col-span-2">
            <UFormGroup class="mb-3" name="email">
              <UInput v-model="form['email']" placeholder="Email" required />
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
      :rows="filtredUsers"
    >
      <template #id-data="{ row }">{{ row.id }}</template>
      <template #fullname-data="{ row }">{{ row.fullname }}</template>
      <template #username-data="{ row }">
        <UDropdown :items="items">
          <UButton
            variant="link"
            :label="row.username"
            @click="userId = row.id"
          />
        </UDropdown>
      </template>
      <template #region-data="{ row }">
        <USelect
          v-model="region"
          :placeholder="row.region"
          :options="[
            'Главный офис',
            'РЦ Юг',
            'РЦ Запад',
            'РЦ Урал',
            'РЦ Восток',
          ]"
          @change="userAction(region, row.id)"
        />
      </template>
      <template #role-data="{ row }">
        <USelect
          v-model="role"
          :placeholder="row.role"
          :options="['admin', 'user', 'guest']"
          @change="userAction(role, row.id)"
        />
      </template>
      <template #created-data="{ row }">{{
        new Date(row.created).toLocaleDateString("ru-RU")
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
        new Date(row.pswd_create).toLocaleDateString("ru-RU")
      }}</template>
      <template #change_pswd-data="{ row }">
        <div class="text-center">
          <UChip size="2xl" :color="row.change_pswd ? 'red' : 'green'" />
        </div>
      </template>
    </UTable>
  </div>
</template>
