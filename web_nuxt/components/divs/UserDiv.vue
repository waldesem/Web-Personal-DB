<script setup lang="ts">
import type { User } from "@/types";

const toast = useToast();

const authFetch = useFetchAuth();

const region = ref("");
const role = ref("");

const props = defineProps({
  user: {
    type: Object as () => User,
    default: {} as User,
  },
});

const emit = defineEmits(["update", "cancel"]);

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
      color: "error",
    });
    return;
  }
  const { message } = (await authFetch("/route/user/" + id, {
    params: {
      item: item,
    },
  })) as Record<string, string>;
  if (message == "success") {
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: "Действие успешно выполнено",
      color: "success",
    });
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Действие не было выполнено",
      color: "error",
    });
  }
  emit("update", id);
}
</script>

<template>
  <ElementsCardDiv>
    <ElementsLabelSlot :label="'ID'">{{ props.user.id }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Пользователь'">{{
      props.user.fullname
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Логин'">
      {{ props.user.username }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Email'">{{
      props.user.email
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Регион'">
      <USelect
        v-model="region"
        :placeholder="props.user.region"
        :options="['Главный офис', 'РЦ Юг', 'РЦ Запад', 'РЦ Урал', 'РЦ Восток']"
        @change="userAction(region, props.user.id)"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Роль'">
      <USelect
        v-model="role"
        :placeholder="props.user.role"
        :options="['admin', 'api', 'user', 'guest']"
        @change="userAction(role, props.user.id)"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Создан'">{{
      new Date(props.user.created).toLocaleString("ru-RU")
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Попытка'">{{
      props.user.attempt
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Блок'">{{
      props.user.blocked ? "Да" : "Нет"
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Обновлен'">{{
      new Date(props.user.pswd_create).toLocaleString("ru-RU")
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Изм.пароля'"
      >{{ props.user.change_pswd ? "Да" : "Нет" }}
    </ElementsLabelSlot>
    <UButtonGroup class="mt-3">
      <UButton
        :label="props.user.deleted ? 'Восстановить' : 'Удалить'"
        color="error"
        variant="outline"
        type="button"
        @click="userAction('delete', props.user.id)"
      />
      <UButton
        :label="props.user.blocked ? 'Разблокировать' : 'Заблокировать'"
        color="primary"
        variant="outline"
        @click="userAction('block', props.user.id)"
      />
      <UButton
        label="Сбросить пароль"
        color="warning"
        variant="outline"
        @click="userAction('reset', props.user.id)"
      />
      <UButton
        label="Выход"
        color="success"
        variant="outline"
        @click="emit('cancel')"
      />
    </UButtonGroup>
  </ElementsCardDiv>
</template>
