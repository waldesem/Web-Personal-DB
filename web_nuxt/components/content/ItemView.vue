<script setup lang="ts">
import type { AsyncDataRequestStatus } from "nuxt/app";
import type { Item } from "@/types";

interface Response {
  message: AsyncDataRequestStatus;
}

// Импортируем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

const toasts = useToasts();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  icon: {
    type: String,
    required: true,
  },
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
const { data, status, refresh } = await useLazyAsyncData(props.view, () =>
  $api<Item[]>(`/routes/items/${props.view}/${candId.value}`)
);

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  status.value = "pending";
  modal.value = false;
  const { message } = (await $api(
    `/routes/items/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Response;
  item.value = {};
  await refresh();
  if (message === "success") {
    toasts.create("success", "Информация успешно обновлена");
  } else toasts.create();
}

// Определяем функцию для удаления данных
async function deleteItem(id: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  status.value = "pending";
  const { message } = (await $api(`/routes/items/${props.view}/${id}`, {
    method: "DELETE",
  })) as Response;
  await refresh();
  if (message === "success") {
    toasts.create("success", "Информация успешно удалена");
  } else toasts.create();
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty
    v-if="!data?.length"
    :icon="props.icon"
    title="Данные отсутствуют"
    size="sm"
  >
    <template #body>
      <UButton
        v-if="editable"
        :loading="status == 'pending'"
        icon="i-lucide-list-plus"
        label="Добавить запись"
        variant="outline"
        size="sm"
        @click="modal = true"
      />
    </template>
  </UEmpty>

  <Suspense>
    <template #default>
      <div v-for="(content, index) in data" :key="index" class="ms-2 py-2">
        <!-- Выводим кнопки редактирования/удаления данных, в режиме редактирования -->
        <LazyElementsDivMenu
          v-if="editable"
          @update="
            item = content as object;
            modal = true;
          "
          @delete="deleteItem(content['id'])"
        />
        <!-- Выводим элемент данных -->
        <slot name="item" :item-content="content" />
        <USeparator v-if="data && index < data.length - 1" />
      </div>
    </template>

    <template v-if="data" #fallback>
      <div v-for="d in data.length + 1" :key="d">
        <ElementsLabelValue v-for="row in props.rows" :key="row">
          <template #label>
            <USkeleton class="h-6" />
          </template>
          <USkeleton class="h-6 w-[300px]" />
        </ElementsLabelValue>
        <USeparator v-if="d < data.length" />
      </div>
    </template>
  </Suspense>

  <!-- Модальное окно для редактирования данных -->
  <UModal
    v-model:open="modal"
    title="Данные профиля"
    description="Введите или отредактируйте данные"
  >
    <UButton
      v-if="editable && data?.length"
      :loading="status == 'pending'"
      class="mt-2"
      label="Добавить запись"
      icon="i-lucide-plus"
      variant="outline"
      size="sm"
      block
    />
    <template #body>
      <slot name="form" :form-content="item" :submit-item="submitItem" />
    </template>
  </UModal>
</template>
