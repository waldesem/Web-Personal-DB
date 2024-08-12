<script setup lang="ts">
import { computed, onBeforeMount, ref } from "vue";
import { debounce } from "@/utils/utilities";
import { server, stateAlert, stateClassify } from "@/state/state";
import type { User } from "@/utils/interfaces";
import { useFetchAuth } from "@/utils/auth";

const classifyState = stateClassify();
const alertState = stateAlert();

onBeforeMount(async () => {
  await getUsers();
});

const users = computed(() => {
  return dataUsers.value.users.filter(
    (user: User) => user.deleted == dataUsers.value.viewDeleted
  );
});

const isCollapsed = ref(false);

const dataUsers = ref({
  search: "",
  userId: "",
  region: "",
  role: "",
  users: [] as User[],
  form: {} as User,
  viewDeleted: false,
});

async function getUsers() {
  try {
    const fetchAuth = useFetchAuth();
    const data = await fetchAuth(`${server}/users`, {
      params: {
        search: dataUsers.value.search,
      },
    });
    dataUsers.value.users = data as unknown as User[];
  } catch (error: unknown) {
    console.error(error);
  }
}

async function userAction(
  item: string,
  id: string = dataUsers.value.userId
): Promise<void> {
  const matched = {
    delete: "удалить/восстановить",
    drop: "сбросить пароль",
    block: "заблокировать/разблокировать",
  };
  if (item === "delete") {
    if (!confirm(`Вы действительно хотите ${matched[item]} пользователя?`)) {
      return;
    }
  }
  try {
    const fetchAuth = useFetchAuth();
    const response = await fetchAuth(`${server}/users/${id}`, {
      params: {
        item: item,
      },
    });
    console.log(response);
    Object.assign(dataUsers.value, {
      userId: "",
      region: "",
      role: "",
    })
    getUsers();
  } catch (error: unknown) {
    alertState.setAlert("rose", "Внимание", "Невозможно выполнить операцию");
    console.error(error);
  }
}

async function submitUser(): Promise<void> {
  try {
    const fetchAuth = useFetchAuth();
    const response = await fetchAuth(`${server}/users`, {
      method: "POST",
      body: dataUsers.value.form,
    });
    console.log(response);
    isCollapsed.value = false;
    alertState.setAlert("green", "Успешно", "Пользователь успешно создан");
    getUsers();
  } catch (error) {
    alertState.setAlert("rose", "Внимание", "Ошибка при создании пользователя");
    console.error(error);
  }
}

const searching = debounce(() => {
  getUsers();
}, 500);

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
  <LayoutsMenu>
    <div class="py-8">
      <h3 class="text-2xl text-gray-600 font-bold">Пользователи</h3>
    </div>
    <div class="mb-8">
      <UInput
        v-model="dataUsers.search"
        size="lg"
        placeholder="Поиск по имени пользователя"
        @input.prevent="searching"
      />
    </div>
    <div class="flex items-center justify-between mb-4">
      <UToggle v-model="dataUsers.viewDeleted" :label="'Показать удаленные'" />
      <UButton
        variant="link"
        label="Добавить пользователя"
        @click="isCollapsed = !isCollapsed"
      />
    </div>
    <Transition name="slide-fade">
      <UForm
        v-if="isCollapsed"
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
        <UChip size="2xl" :color="row.blocked ? 'red' : 'green'"/>
      </template>
      <template #pswd_create-data="{ row }">{{
        new Date(row.pswd_create).toLocaleDateString()
      }}</template>
      <template #change_pswd-data="{ row }">
        <UChip size="2xl" :color="row.change_pswd ? 'red' : 'green'"/>
      </template>
    </UTable>
  </LayoutsMenu>
</template>
