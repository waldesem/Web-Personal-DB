<script setup lang="ts">
import { watchDebounced } from "@vueuse/core";
import { z } from "zod";
import type { User } from "@/types";

type UserForm = z.infer<typeof schema>;

const toast = useToast();

const fetchAuth = useFetchAuth();

const search = ref("");
const region = ref("");
const role = ref("");
const users = ref([] as User[]);
const user = ref({} as User);
const form = ref({} as UserForm);
const modalForm = ref(false);
const modalProfile = ref(false);
const viewDeleted = ref(false);

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

async function openUser(id: string): Promise<void> {
  user.value = (await fetchAuth("/route/user/" + id, {
    params: {
      item: "open",
    },
  })) as User;
  modalProfile.value = true;
}

/**
 * Performs an action on a user, such as blocking or deleting them.
 *
 * @param {string} item The action to perform
 * @param {string} id The ID of the user to perform the action on
 * @returns {Promise<void>}
 */
async function userAction(item: string, id: string): Promise<void> {
  if (id == stateUser.value.id) {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Невозможно  выполнить действие",
      color: "red",
    });
    clearItems();
    return;
  }
  if (!confirm("Подтвердите действие!")) {
    clearItems();
    return;
  }
  const { message } = (await fetchAuth("/route/user/" + id, {
    params: {
      item: item,
    },
  })) as Record<string, string>;
  clearItems();
  await openUser(id);
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

const clearItems = () => {
  region.value = "";
  role.value = "";
};

/**
 * Submits a new user to the server.
 * @returns {Promise<void>}
 */
async function submitUser(): Promise<void> {
  const { message } = (await fetchAuth("/route/users", {
    method: "POST",
    body: form.value,
  })) as Record<string, string>;
  modalForm.value = false;
  form.value = {} as UserForm;
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
</script>

<template>
  <div class="mb-6">
    <ElementsHeaderDiv
      :cls="'text-2xl text-gray-500'"
      :header="'ПОЛЬЗОВАТЕЛИ'"
    />
    <div class="my-6">
      <UInput v-model="search" placeholder="Поиск по имени пользователя" />
    </div>
    <div class="flex items-center justify-between mb-4">
      <UToggle v-model="viewDeleted" :label="'Показать удаленные'" />
      <UButton
        variant="link"
        label="Добавить пользователя"
        @click="modalForm = true"
      />
    </div>
    <UModal v-model="modalForm">
      <ElementsCardDiv>
        <UForm :schema="schema" :state="form" @submit.prevent="submitUser">
          <UFormGroup
            class="mb-3"
            label="Имя пользователя"
            name="fullname"
            required
          >
            <UInput
              v-model="form['fullname']"
              placeholder="Имя пользователя"
              required
            />
          </UFormGroup>
          <UFormGroup class="mb-3" label="Логин" name="username">
            <UInput v-model="form['username']" placeholder="Логин" required />
          </UFormGroup>
          <UFormGroup class="mb-3" label="Email" name="email">
            <UInput v-model="form['email']" placeholder="Email" required />
          </UFormGroup>
          <ElementsBtnGroup @cancel="modalForm = false" />
        </UForm>
      </ElementsCardDiv>
    </UModal>

    <UModal v-model="modalProfile" prevent-close>
      <ElementsCardDiv>
        <ElementsLabelSlot :label="'ID'">{{ user["id"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Пользователь'">{{
          user["fullname"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Логин'">
          {{ user["username"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Email'">{{
          user["email"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Регион'">
          <USelect
            v-model="region"
            :placeholder="user.region"
            :options="[
              'Главный офис',
              'РЦ Юг',
              'РЦ Запад',
              'РЦ Урал',
              'РЦ Восток',
            ]"
            @change="userAction(region, user.id)"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Роль'">
          <USelect
            v-model="role"
            :placeholder="user.role"
            :options="['admin', 'user', 'guest']"
            @change="userAction(role, user.id)"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Создан'">{{
          new Date(user["created"]).toLocaleString("ru-RU")
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Попытка'">{{
          user["attempt"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Блок'">{{
          user["blocked"] ? "Да" : "Нет"
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Обновлен'">{{
          new Date(user["pswd_create"]).toLocaleString("ru-RU")
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Изм.пароля'"
          >{{ user["change_pswd"] ? "Да" : "Нет" }}
        </ElementsLabelSlot>
        <UButtonGroup class="mt-3">
          <UButton
            :label="user.deleted ? 'Восстановить' : 'Удалить'"
            color="red"
            variant="outline"
            type="button"
            @click="userAction('delete', user.id)"
          />
          <UButton
            :label="user.blocked ? 'Разблокировать' : 'Заблокировать'"
            color="blue"
            variant="outline"
            @click="userAction('block', user.id)"
          />
          <UButton
            label="Сбросить пароль"
            color="gray"
            variant="outline"
            @click="userAction('drop', user.id)"
          />
          <UButton
            label="Выход"
            color="green"
            variant="outline"
            @click="
              modalProfile = false;
              user = {} as User;
              refresh();
            "
          />
        </UButtonGroup>
      </ElementsCardDiv>
    </UModal>

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
      @select="openUser($event[0])"
    >
      <template #id-data="{ row }">{{ row.id }}</template>
      <template #fullname-data="{ row }">{{ row.fullname }}</template>
      <template #username-data="{ row }">{{ row.username }}</template>
      <template #region-data="{ row }">{{ row.region }}</template>
      <template #role-data="{ row }">{{ row.role }}</template>
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
          <UIcon
            :name="
              row.blocked ? 'i-heroicons-lock-closed' : 'i-heroicons-lock-open'
            "
          />
        </div>
      </template>
      <template #pswd_create-data="{ row }">{{
        new Date(row.pswd_create).toLocaleDateString("ru-RU")
      }}</template>
      <template #change_pswd-data="{ row }">
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
