<script setup lang="ts">
import type { Person } from "@/types";

const toasts = useToasts();

const { $api } = useNuxtApp();

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
});

const lock = useLock();

const modal = ref(false); // Объявляем переменную модального окна

// Определяем функцию для отправки данных формы на сервер
async function submitPerson(form: Person) {
  modal.value = false;
  const { status } = await $api.raw("/routes/persons/" + props.person.id, {
    method: "PATCH",
    body: form,
  });
  if (status === 200) {
    toasts.create("success", "Информация успешно обновлена");
    refreshNuxtData("person");
  } else {
    toasts.create();
  }
}

// Определяем функцию для удаления данных
async function deletePerson() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  if (!confirm("Все данные будут удалены безвозвратно!?")) return;
  const { status } = await $api.raw(`/routes/persons/${props.person.id}`, {
    method: "DELETE",
  });
  if (status === 204) {
    toasts.create("success", "Информация успешно удалена");
    refreshNuxtData("candidates");
    return navigateTo("/persons");
  }
  toasts.create();
}
</script>

<template>
  <div class="ms-2 mt-2">
    <!-- Выводим кнопки редактирования или удаления данных -->
    <LazyElementDivMenu
      v-if="!lock"
      @update="modal = true"
      @delete="deletePerson()"
    />
    <ItemsPersonDiv :item="props.person" />
    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      title="Aнкета"
      description="Редактирование анкетные данные"
    >
      <template #body>
        <LazyFormsResumeForm :resume="props.person" @update="submitPerson" />
      </template>
    </UModal>
  </div>
</template>
