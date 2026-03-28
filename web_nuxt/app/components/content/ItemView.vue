<script setup lang="ts">
import type { Items } from "@/types";

const toasts = useToasts();

const itemStore = useItemStore();

const editStore = useEditStore();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
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

// Объявляем переменные для работы с данными
const item = shallowRef<object>({}); // Данные для передачи в форму и редактирования
const itemId = ref<string>("");
const modal = ref(false); // Флаг для открытия модального окна
const status = ref("success"); // Статус запроса
const method = ref<"POST" | "PATCH">("POST");

// Определяем функцию для получения данных из API
async function getItem() {
  status.value = "pending";
  await itemStore.getItem(props.view);
  status.value = "success";
}

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  status.value = "pending";
  modal.value = false;
  const response =
    method.value === "POST"
      ? await itemStore.addItem(props.view, form)
      : await itemStore.editItem(props.view, itemId.value, form);
  if (response?.status === 200 || response?.status === 201) {
    toasts.create("success", "Информация успешно обновлена");
  } else toasts.create();
  item.value = {};
  await getItem();
}

// Определяем функцию для удаления данных
async function deleteItem(itemId: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  status.value = "pending";
  const resp = await itemStore.deleteItem(props.view, itemId);
  if (resp?.status === 204) {
    await getItem();
    toasts.create("success", "Информация успешно удалена");
  } else {
    toasts.create();
  }
  status.value = "success";
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty
    v-if="!itemStore.items[props.view]?.length"
    :icon="props.icon"
    class="m-4"
    title="Данные отсутствуют"
    size="sm"
  >
    <template #body>
      <UButton
        v-if="editStore.editable"
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
      <div
        v-for="(content, index) in itemStore.items[props.view]"
        :key="index"
        class="mx-2 py-2"
      >
        <!-- Выводим кнопки редактирования/удаления данных, в режиме редактирования -->
        <LazyElementDivMenu
          v-if="editStore.editable"
          @update="
            item = content;
            method = 'PATCH';
            modal = true;
            itemId = content.id;
          "
          @delete="deleteItem(content.id)"
        />
        <!-- Выводим элемент данных -->
        <component :is="ItemComponent" :item="content" />
        <USeparator v-if="index + 1 < itemStore.items[props.view].length" />
      </div>
    </template>

    <template #fallback>
      <div v-for="len in itemStore.items[props.view]?.length + 1" :key="len">
        <ElementSkeletonDiv />
        <USeparator v-if="len < itemStore.items[props.view].length" />
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
      v-if="editStore.editable && itemStore.items[props.view]?.length"
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
