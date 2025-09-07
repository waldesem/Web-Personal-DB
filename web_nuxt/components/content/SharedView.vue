<script setup lang="ts">
// Импортируем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  view: {
    type: String,
    required: true,
  },
  rows: {
    type: Number,
    default: 3,
  },
});

// Инжектируем данные (id кандидата и доступна ли анкета для редактирования)
const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

// Объявляем переменные для работы с данными
const item = shallowRef({} as object); // Данные для передачи в форму и редактирования
const modal = ref(false); // Флаг для открытия модального окна

// Определяем Composable для получения данных из API
const { data, status, refresh } = await useLazyAsyncData(
  props.view,
  async () => {
    return (await $api(`/routes/items/${props.view}/${candId.value}`)) as object[];
  }
);

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  status.value = "pending";
  const { message } = await $api<Record<string, string>>(
    `/routes/items/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  );
  await refresh();
  status.value = message as "success" | "error";
  item.value = {};
  if (message == "success") {
    useToasts(message, "Информация успешно обновлена");
  } else {
    useToasts();
  }
}

// Определяем функцию для удаления данных
async function deleteItem(id: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  status.value = "pending";
  const { message } = await $api<Record<string, string>>(
    `/routes/items/${props.view}/${id}`,
    {
      method: "DELETE",
    }
  );
  status.value = message as "success" | "error";
  if (message == "success") {
    useToasts(message, "Информация успешно обновлена");
    await refresh();
  } else {
    useToasts();
  }
}
</script>

<template>
  <!-- Выводим скелетный элемент. если данные ещё не загружены -->
  <div v-if="status === 'pending' && data">
    <div v-for="i in data.length + 1" :key="i">
      <LazyElementsSkeletonDiv :rows="props.rows" />
      <USeparator v-if="i < data.length" />
    </div>
  </div>
  <div v-else>
    <!-- Выводим список элементов с кнопками для редактирования и удаления -->
    <div v-for="(content, index) in data" :key="index" class="py-4 ms-2">
      <!-- Выводим кнопки редактирования или удаления данных если доступно редактирование -->
      <LazyElementsDivMenu
        v-if="editable"
        @update="
          item = content;
          modal = true;
        "
        @refresh="deleteItem(content['id' as keyof typeof content])"
      />

      <!-- Выводим элемент данных -->
      <slot name="item" :item-content="content" />
      <USeparator v-if="data && index < data.length - 1" />
    </div>

    <!-- Выводим сообщение если данные отсутствуют -->
    <div v-if="!data || !data.length" class="p-4 text-red-800">
      Данные отсутствуют
    </div>
  </div>

  <!-- Модальное окно для редактирования данных -->
  <UModal
    v-model:open="modal"
    title="Данные профиля"
    description="Введите или отредактируйте данные"
  >
    <div
      v-if="editable"
      class="flex justify-start py-2"
      :class="{ 'border-t border-gray-200': data && data.length > 0 }"
    >
      <UButton
        :loading="status == 'pending'"
        label="Добавить запись"
        icon="i-lucide-file-plus"
        variant="ghost"
      />
    </div>
    <template #body>
      <slot name="form" :form-content="item" :submit-item="submitItem" />
    </template>
  </UModal>
</template>
