<script setup lang="ts">
import type { Person } from "@/types";

const toasts = useToasts();

const edit = useEditStore();

const person = usePersonStore();

const modal = ref(false); // Объявляем переменную модального окна

const state = ref(""); // Объявляем переменную статуса

// Определяем функцию для отправки данных формы на сервер
async function submitPerson(form: Person) {
  modal.value = false;
  state.value = "pending";
  const { status } = await person.editPerson(form);
  if (status === 200) {
    toasts.create("success", "Информация успешно обновлена");
    refreshNuxtData("person");
  } else {
    toasts.create();
  }
  state.value = "";
}

// Определяем функцию для удаления данных
async function deletePerson() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  if (!confirm("Все данные будут удалены безвозвратно!?")) return;
  state.value = "pending";
  const { status } = await person.deletePerson();
  state.value = "";
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
      v-if="edit.locked"
      @update="modal = true"
      @delete="deletePerson()"
    />

    <!-- Выводим данные или скелетный элемент -->
    <Suspense>
      <template #default>
        <ItemsPersonDiv :item="person.data" />
      </template>
      <template #fallback>
        <ElementSkeletonDiv :rows="12" />
      </template>
    </Suspense>

    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      title="Aнкета"
      description="Редактирование анкетные данные"
    >
      <template #body>
        <FormsResumeForm :resume="person.data" @update="submitPerson" />
      </template>
    </UModal>
  </div>
</template>
