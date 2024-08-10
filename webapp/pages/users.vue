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
    alertState.setAlert("alert-warning", "Невозможно выполнить операцию");
    console.error(error);
  }
}

async function submitUser(): Promise<void> {
  try {
    const fetchAuth = useFetchAuth();
    const response = await fetchAuth(`${server}/users`, dataUsers.value.form);
    console.log(response);
    alertState.setAlert("alert-success", "Пользователь успешно создан");
    cancelOperations();
    getUsers();
  } catch (error) {
    alertState.setAlert(
      "alert-warning",
      "Возможно, пользователь уже существует"
    );
    console.error(error);
  }
}

function cancelOperations() {
  Object.keys(dataUsers.value.profile).forEach(
    (key) => delete dataUsers.value[key as keyof typeof dataUsers.value]
  );
}
</script>

<template>
  <LayoutsMenu>
    <div class="py-5">
      <h3 class="text-2xl text-opacity-75 text-grey-600 font-bold">
        Список пользователей
      </h3>
    </div>
    <UInput
      v-model="dataUsers.search"
      placeholder="Поиск по имени пользователя"
      @input.prevent="searching"
    />
    <div class="d-flex justify-content-between">
      <UToggle v-model="dataUsers.viewDeleted" :label="'Показать удаленные'" />
      <UDropdown>
        <UButton
          color="white"
          label="Добавить пользователя"
          trailing-icon="i-heroicons-chevron-down-20-solid"
        />
        <UForm @submit.prevent="submitUser">
          <UFormGroup class="mb-3" size="md" label="Имя пользователя" required>
            <UInput
              v-model="dataUsers.form['fullname']"
              placeholder="Имя пользователя"
            />
          </UFormGroup>
          <UFormGroup class="mb-3" size="md" label="Логин" required>
            <UInput v-model="dataUsers.form['username']" placeholder="Логин" />
          </UFormGroup>
          <ElementsBtnGroup :offset="false" />
        </UForm>
      </UDropdown>
    </div>
    <table :tbl-class="'table align-middle'">
      <thead>
        <tr>
          <th width="5%">#</th>
          <th>Имя пользователя</th>
          <th width="15%">Логин</th>
          <th width="10%">Блокировка</th>
          <th width="15%">Создан</th>
          <th width="15%">Роль</th>
          <th width="20%">Регион</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td colspan="7">
            <table
              id="overflow"
              :tbl-class="'table table-hover align-middle no-bottom-border'"
            >
              <tbody>
                <tr v-for="user in users" :key="user.id" height="50px">
                  <td width="5%">{{ user.id }}</td>
                  <td>{{ user.fullname }}</td>
                  <td width="15%">
                    <UButton variant="link" @click="isOpen = true">
                      {{ user.username }}
                    </UButton>
                  </td>
                  <td width="10%">{{ user.blocked ? "Да" : "Нет" }}</td>
                  <td width="15%">
                    {{ new Date(user.pswd_create).toLocaleString() }}
                  </td>
                  <td width="15%">
                    {{ user.role }}
                  </td>
                  <td width="20%">{{ user.region }}</td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
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
            :options="classifyState.classes.value.regions"
            @change="userAction(dataUsers.profile.region)"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Роль'">
          <USelect
            v-model="dataUsers.profile['role']"
            :select="classifyState.classes.value.roles"
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
#overflow {
  max-height: 50vh;
  overflow-y: auto;
}
.no-bottom-border td {
  border-bottom: none;
}
</style>
