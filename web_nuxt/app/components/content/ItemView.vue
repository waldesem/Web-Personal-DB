<script setup lang="ts">
import type { Items } from "@/types";

const { $api } = useNuxtApp();

const toasts = useToasts();

const editable = inject("editable");

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  data: {
    type: Array as PropType<Items[keyof Items]>,
    default: () => [],
  },
  icon: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  view: {
    type: String as PropType<keyof Items>,
    required: true,
  },
});

const ItemComponent = defineAsyncComponent<Component>(
  () => import(`../items/${capitalize(props.view)}Item.vue`),
);
const FormComponent = defineAsyncComponent<Component>(
  () => import(`../forms/${capitalize(props.view)}Form.vue`),
);

// Инжектируем данные (id кандидата и доступна ли анкета для редактирования)
const candId = inject("candId") as Ref<string>;

// Объявляем переменные для работы с данными
const data = shallowRef(props.data); // Данные для вывода
const item = shallowRef<object>({}); // Данные для передачи в форму и редактирования
const itemId = ref<string | null>(null);
const modal = ref(false); // Флаг для открытия модального окна
const status = ref("success"); // Статус запроса
const method = ref("POST") as Ref<"POST" | "PATCH">;

// Определяем функцию для получения данных из API
async function getItem() {
  status.value = "pending";
  data.value = await $api(`/routes/items/${props.view}/${candId.value}`);
  status.value = "success";
}

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  status.value = "pending";
  modal.value = false;
  const url = `/routes/items/${candId.value}`;
  const response = await $api.raw(
    method.value === "POST" ? url : `${url}/${itemId.value}`,
    {
      method: method.value,
      body: { item: { ...form, item: props.view } }, // add discriminator for backend validation
    },
  );
  item.value = {};
  await getItem();
  if (response.status === 201) {
    toasts.create("success", "Информация успешно обновлена");
  } else toasts.create();
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  status.value = "pending";
  try {
    const { status } = await $api.raw(`/routes/items/${props.view}/${itemId}`, {
      method: "DELETE",
    });
    if (status === 204) {
      await getItem();
      toasts.create("success", "Информация успешно удалена");
    }
  } catch (error) {
    console.error(error);
  }
  toasts.create();
  status.value = "success";
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty
    v-if="!data?.length"
    :icon="props.icon"
    class="m-4"
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
        @click="
          modal = true;
          method = 'POST';
        "
      />
    </template>
  </UEmpty>

  <Suspense>
    <template #default>
      <div v-for="(content, index) in data" :key="index" class="mx-2 py-2">
        <!-- Выводим кнопки редактирования/удаления данных, в режиме редактирования -->
        <LazyElementDivMenu
          v-if="editable"
          @update="
            item = content;
            method = 'PATCH';
            modal = true;
            itemId = content.id
          "
          @delete="deleteItem(content.id)"
        />
        <!-- Выводим элемент данных -->
        <component :is="ItemComponent" :item="content" />
        <USeparator v-if="index + 1 < data.length" />
      </div>
    </template>

    <template #fallback>
      <div v-for="len in data?.length + 1" :key="len">
        <ElementSkeletonDiv />
        <USeparator v-if="len < data.length" />
      </div>
    </template>
  </Suspense>

  <!-- Модальное окно для редактирования данных -->
  <UModal
    v-model:open="modal"
    :title="props.title"
    description="Добавить/редактировать данные"
  >
    <UButton
      v-if="editable && data?.length"
      :loading="status == 'pending'"
      class="mb-2"
      label="Добавить запись"
      icon="i-lucide-plus"
      variant="outline"
      color="neutral"
      size="sm"
      block
      @click="method = 'POST'"
    />
    <template #body>
      <component :is="FormComponent" :item="item" @update="submitItem" />
    </template>
  </UModal>
</template>
