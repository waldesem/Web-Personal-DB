<script setup lang="ts">
import type { FetchResponse } from "ofetch";
import type { PersonExt, PersonId } from "@/types";

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

const { data: person } = useNuxtData<PersonExt>("person");

const toasts = useToasts();

const editable = inject("editable");

const modal = ref(false); // Объявляем переменную модального окна

const status = ref("success"); // Объявляем переменную статуса

// Определяем функцию для отправки данных формы на сервер
function submitPerson(response: FetchResponse<Partial<PersonId>>) {
  modal.value = false;
  status.value = "pending";
  refreshNuxtData("person");
  status.value = "success";
  if (response.status === 200) {
    toasts.create("success", "Информация успешно обновлена");
  } else {
    toasts.create();
  }
}

// Определяем функцию для удаления данных
async function deletePerson() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  if (!confirm("Все данные будут удалены безвозвратно!?")) return;
  status.value = "pending";
  try {
    const { status } = await $api.raw<Record<string, string>>(
      `/routes/persons/${person.value?.id}`,
      {
        method: "DELETE",
      },
    );
    if (status === 204) {
      toasts.create("success", "Информация успешно удалена");
      refreshNuxtData("candidates");
      return navigateTo("/persons");
    }
  } catch (error) {
    console.error(error);
  }
  refreshNuxtData("person");
  toasts.create();
  status.value = "error";
}
</script>

<template>
  <div class="ms-2 mt-2">
    <!-- Выводим кнопки редактирования или удаления данных -->
    <LazyElementDivMenu
      v-if="editable"
      @update="modal = true"
      @delete="deletePerson()"
    />

    <!-- Выводим данные или скелетный элемент -->
    <Suspense>
      <template #default>
        <ItemsPersonDiv :item="person" />
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
        <FormsResumeForm
          :resume="person"
          :method="'PATCH'"
          @pending="status = 'pending'"
          @update="submitPerson"
        />
      </template>
    </UModal>
  </div>
</template>
