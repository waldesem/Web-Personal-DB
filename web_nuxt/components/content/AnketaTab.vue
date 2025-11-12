<script setup lang="ts">
import type { Person } from "@/types";
import type { AsyncDataRequestStatus } from "nuxt/app";

const toasts = useToasts();

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
  status: {
    type: String as PropType<AsyncDataRequestStatus>,
    default: "success",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

// Преобразуем переменную для чтения в реактивную
const status = toRef(props.status);

// Объявляем переменную для переключения модального окна
const modal = ref(false);

// Определяем функцию для отправки данных формы на сервер
function submitPerson(person_id: number | null) {
  modal.value = false;
  refreshNuxtData("person");
  if (person_id) {
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
  const { message } = await $api<Record<string, string>>(
    `/routes/persons/${props.person.id}`,
    { method: "DELETE" }
  );
  if (message == "success") {
    toasts.create("success", "Информация успешно удалена");
    refreshNuxtData("candidates");
    await navigateTo("/persons");
  } else {
    refreshNuxtData("person");
    toasts.create();
  }
}
</script>

<template>
  <div class="ms-2 mt-4">
    <!-- Выводим кнопки редактирования или удаления данных -->
    <LazyElementsDivMenu
      v-if="editable"
      @update="modal = true"
      @delete="deletePerson()"
    />

    <!-- Выводим данные или скелетный элемент -->
    <Suspense>
      <template #default>
        <ItemsPersonItem :item="props.person" />
      </template>
      <template #fallback>
        <ElementsLabelValue v-for="row in 12" :key="row">
          <template #label>
            <USkeleton class="h-6" />
          </template>
          <USkeleton class="h-6 w-[300px]" />
        </ElementsLabelValue>
      </template>
    </Suspense>

    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-model:open="modal"
      title="Редактирование анкеты"
      description="Отредактируйте анкетные данные"
    >
      <template #body>
        <FormsResumeForm
          :resume="props.person"
          @pending="status = 'pending'"
          @update="submitPerson"
        />
      </template>
    </UModal>
  </div>
</template>
