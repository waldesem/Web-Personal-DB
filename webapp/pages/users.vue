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

const isOpen = ref(false);
const isCollapsed = ref(false);

const dataUsers = ref({
  search: "",
  users: [] as User[],
  profile: {} as User,
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

const searching = debounce(() => {
  getUsers();
}, 500);

async function userAction(item: string): Promise<void> {
  if (item === "delete") {
    if (
      !confirm("Вы действительно хотите удалить/восстановить пользователя?")
    ) {
      return;
    }
  }
  try {
    const fetchAuth = useFetchAuth();
    const response = await fetchAuth(
      `${server}/users/${dataUsers.value.profile.id}`,
      {
        params: {
          item: item,
        },
      }
    );
    console.log(response);
    getUsers();
  } catch (error: unknown) {
    alertState.setAlert("red", "Внимание", "Невозможно выполнить операцию");
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
    alertState.setAlert("red", "Внимание", "Ошибка при создании пользователя");
    console.error(error);
  }
}
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
              />
            </UFormGroup>
          </div>
          <div class="col-span-2">
            <UFormGroup required class="mb-3">
              <UInput
                v-model="dataUsers.form['username']"
                placeholder="Логин"
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
            />
          </div>
        </div>
      </UForm>
    </Transition>
    <UTable
      :columns="[
        { key: 'id', label: '#' },
        { key: 'fullname', label: 'Имя пользователя' },
        { key: 'username', label: 'Логин' },
        { key: 'change_pswd', label: 'Изменить пароль' },
        { key: 'blocked', label: 'Блокировка' },
        { key: 'created', label: 'Создан' },
        { key: 'role', label: 'Роль' },
        { key: 'region', label: 'Регион' },
      ]"
      :rows="users"
    >
      <template #id-data="{ row }">{{ row.id }}</template>
      <template #fullname-data="{ row }">{{ row.fullname }}</template>
      <template #username-data="{ row }"
        ><UButton variant="link" @click="isOpen = true">
          {{ row.username }}
        </UButton></template
      >
      <template #change_pswd-data="{ row }">{{ row.change_pswd }}</template>
      <template #blocked-data="{ row }">
        <UIcon
          v-if="row.blocked"
          name="i-heroicons-face-frown"
          class="w-6 h-6"
        />
        <UIcon v-else name="i-heroicons-face-smile" class="w-6 h-6" />
      </template>
      <template #created-data="{ row }">{{
        new Date(row.created).toLocaleDateString()
      }}</template>
      <template #role-data="{ row }">{{ row.role }}</template>
      <template #region-data="{ row }">{{ row.region }}</template>
    </UTable>
    <UModal v-model="isOpen">
      <UCard>
        <template #header>
          <ElementsLabelSlot :label="'ID'">
            {{ dataUsers.profile.id }}
          </ElementsLabelSlot>
        </template>
        <ElementsLabelSlot :label="'Регион'">
          <USelect
            v-model="dataUsers.profile.region"
            :options="Object.values(classifyState.classes.value.regions)"
            @change="userAction(dataUsers.profile.region)"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Роль'">
          <USelect
            v-model="dataUsers.profile['role']"
            :options="Object.values(classifyState.classes.value.roles)"
            @submit-data="userAction(dataUsers.profile.role)"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Имя пользователя'">
          {{ dataUsers.profile.fullname }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Логин'">
          {{ dataUsers.profile.username }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата создания пароля'">
          {{
            new Date(dataUsers.profile.pswd_create + " UTC").toLocaleString(
              "ru-RU"
            )
          }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Требует смены пароля'">
          {{ dataUsers.profile.change_pswd ? "Да" : "Нет" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Попытки входа'">
          {{ dataUsers.profile.attempt }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Заблокирован'">
          {{ dataUsers.profile.blocked ? "Заблокирован" : "Разблокирован" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Активность'">
          {{ dataUsers.profile.deleted ? "Удален" : "Активен" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Роль'">
          {{ dataUsers.profile.role }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата создания профиля'">
          {{
            new Date(dataUsers.profile.created + " UTC").toLocaleString("ru-RU")
          }}
        </ElementsLabelSlot>
        <template #footer>
          <UButtonGroup size="md" orientation="horizontal">
            <UButton
              label="Сбросить пароль"
              color="green"
              variant="outline"
              @click="userAction('drop')"
            />
            <UButton
              :label="
                dataUsers.profile.deleted ? 'Заблокировать' : 'Разблокировать'
              "
              color="primary"
              variant="outline"
              @click="userAction('block')"
            />
            <UButton
              :label="
                dataUsers.profile.deleted
                  ? 'Восстановить'
                  : 'Отметить к удалению'
              "
              color="red"
              variant="outline"
              @click="userAction('delete')"
            />
          </UButtonGroup>
        </template>
      </UCard>
    </UModal>
  </LayoutsMenu>
</template>

<style scoped>
table {
  max-height: 50vh;
  overflow-y: auto;
}
</style>
