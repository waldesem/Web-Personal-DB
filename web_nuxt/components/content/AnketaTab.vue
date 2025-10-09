<script setup lang="ts">
import type { Persons } from "@/types";

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  person: {
    type: Object as PropType<Persons>,
    required: true,
  },
  status: {
    type: String as PropType<"idle" | "pending" | "success" | "error">,
    default: "success",
  },
});

// Преобразуем переменную для чтения в реактивную
const status = toRef(props.status);

// Инжектируем данные (находится ли анкета в режиме редактирования)
const editable = inject("editable") as Ref<boolean>;

// Объявляем переменную для переключения модального окна
const modal = ref(false);

// Определяем функцию для отправки данных формы на сервер
function submitPerson(person_id: number | null) {
  modal.value = false;
  if (person_id) {
    status.value = "pending";
    refreshNuxtData("persons");
    useToasts("success", "Информация успешно обновлена");
    status.value = "success";
  } else {
    useToasts();
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
    {
      method: "DELETE",
    }
  );
  if (message == "success") {
    useToasts(message, "Информация успешно удалена");
    clearNuxtData();
    return navigateTo("/persons");
  } else {
    useToasts();
    status.value = "error";
  }
}
</script>

<template>
  <div class="mt-4">
    <!-- Выводим кнопки редактирования или удаления данных если доступно редактирование -->
    <LazyElementsDivMenu
      v-if="editable"
      @update="modal = true"
      @delete="deletePerson()"
    />

    <!-- Выводим скелетный элемент. если данные ещё не загружены -->
    <div class="ps-2">
      <Suspense>
        <template #default>
          <LazyItemsPersonItem :item="props.person" />
        </template>
        <template #fallback>
          <LazyElementsSkeletonDiv :rows="12" />
        </template>
      </Suspense>
    </div>
    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-if="editable"
      v-model:open="modal"
      title="Редактирование анкеты"
      description="Отредактируйте анкетные данные"
    >
      <template #body>
        <!-- Выводим форму для редактирования данных внутри модального окна -->
        <LazyFormsResumeForm :resume="props.person" @update="submitPerson" />
      </template>
    </UModal>

    <USeparator />

    <!-- Выводим аккордеон с данными staffs, educations и т.д. -->
    <slot name="#items" />
  </div>
</template>
