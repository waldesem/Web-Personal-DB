<script setup lang="ts">
import type { AsyncDataRequestStatus } from "nuxt/app";

interface ItemResponse {
  message: AsyncDataRequestStatus;
}

type ItemObject = {
  id: string;
} & {
  [key: string]: string | number | boolean;
};

// Импортируем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

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
const { data, status, refresh } = await useLazyAsyncData(
  props.view,
  async () => {
    return (await $api(
      `/routes/items/${props.view}/${candId.value}`
    )) as ItemObject[];
  }
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
  )) as ItemResponse;
  item.value = {};
  await refresh();
  if (message === "success") {
    useToasts("success", "Информация успешно обновлена");
  } else useToasts();
}

// Определяем функцию для удаления данных
async function deleteItem(id: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  status.value = "pending";
  const { message } = (await $api(`/routes/items/${props.view}/${id}`, {
    method: "DELETE",
  })) as ItemResponse;
  await refresh();
  if (message === "success") {
    useToasts("success", "Информация успешно удалена");
  } else useToasts();
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty
    :icon="!data ? props.icon : ''"
    :title="!data ? 'Данные отсутствуют' : ''"
    :variant="!data ? 'outline' : 'naked'"
  >
    <template #body>
      <UButton
        v-if="editable"
        :loading="status == 'pending'"
        :block="data ? true : false"
        :icon="data ? 'i-lucide-plus' : 'i-lucide-list-plus'"
        label="Добавить запись"
        variant="outline"
        size="sm"
        @click="modal = true"
      />
    </template>
  </UEmpty>

  <Suspense>
    <template #default>
      <div v-for="(content, index) in data" :key="index" class="py-2 ms-2">
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
        <slot :name="`item-${props.view}`" :item-content="content" />
        <USeparator v-if="data && index < data.length - 1" />
      </div>
    </template>

    <template v-if="data" #fallback>
      <div v-for="d in data.length + 1" :key="d">
        <ElementsLabelValue v-for="row in props.rows" :key="row">
          <template #label>
            <USkeleton class="h-6" />
          </template>
          <template #value>
            <USkeleton class="h-6 w-[300px]" />
          </template>
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
    <!-- <div
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
    </div> -->
    <template #body>
      <slot
        :name="`form-${props.view}`"
        :form-content="item"
        :submit-item="submitItem"
      />
    </template>
  </UModal>
</template>
