<script setup lang="ts">
import type { Item, Items } from "@/types";
import type { PropType } from "vue";

const { $api } = useNuxtApp();

const toasts = useToasts();

const personId = inject("personId") as Ref<string>;

const locked = inject("locked") as Ref<boolean>;

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  data: {
    type: Object as PropType<Items[keyof Items]>,
    required: true,
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

// Объявляем переменные для работы с данными
const items = toRef(props.data);
const item = shallowRef({} as Item[keyof Item]); // Данные для передачи в форму
const option = ref<"create" | "edit">("create");
const modal = ref(false); // Флаг для открытия модального окна
const state = ref(""); // Статус запроса

// Определяем функцию для получения данных из API
async function getItem() {
  state.value = "pending";
  items.value = await $api(`/routes/items/${props.view}/${personId.value}`);
  state.value = "";
}

async function addItem(view: keyof Items, form: object) {
  return await $api.raw(`/routes/items/${view}/${personId.value}`, {
    method: "POST",
    body: { ...form, item: view }, // add discriminator for backend validation
  });
}

async function editItem(view: keyof Items, itemId: string, form: object) {
  return await $api.raw(`/routes/items/${view}/${personId.value}/${itemId}`, {
    method: "PATCH",
    body: { ...form, item: view }, // add discriminator for backend validation
  });
}

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  state.value = "pending";
  modal.value = false;
  const { status } =
    option.value === "create"
      ? await addItem(props.view, form)
      : await editItem(props.view, item.value.id, form);
  if (status === 200 || status === 201) {
    toasts.create("success", "Информация успешно обновлена");
  } else toasts.create();
  item.value = {} as Item[keyof Item];
  await getItem();
}

// Определяем функцию для удаления данных
async function deleteItem(id: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  state.value = "pending";
  const { status } = await $api.raw(
    `/routes/items/${props.view}/${personId.value}/${id}`,
    {
      method: "DELETE",
    },
  );
  if (status === 204) {
    toasts.create("success", "Информация успешно удалена");
  } else {
    toasts.create();
  }
  await getItem();
}
</script>

<template>
  <!-- Выводим сообщение если данные отсутствуют -->
  <UEmpty
    v-if="!items.length"
    :icon="props.icon"
    class="m-4"
    title="Данные отсутствуют"
    size="sm"
  >
    <template #body>
      <UButton
        v-if="!locked"
        :loading="state == 'pending'"
        icon="i-lucide-list-plus"
        label="Добавить запись"
        variant="outline"
        size="sm"
        @click="
          modal = true;
          option = 'create';
        "
      />
    </template>
  </UEmpty>

  <Suspense>
    <template #default>
      <div v-for="(content, index) in items" :key="index" class="mx-2 py-2">
        <!-- Выводим кнопки редактирования/удаления данных -->
        <LazyElementDivMenu
          v-if="!locked"
          @update="
            item = content;
            modal = true;
            option = 'edit';
          "
          @delete="deleteItem(content.id)"
        />
        <!-- Выводим элемент данных -->
        <component :is="ItemComponent" :item="content" />
        <USeparator v-if="index + 1 < items.length" />
      </div>
    </template>

    <template #fallback>
      <div v-for="len in items.length + 1" :key="len">
        <ElementSkeletonDiv />
        <USeparator v-if="len < items.length" />
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
      v-if="!locked && items.length"
      :loading="state == 'pending'"
      class="mb-2"
      label="Добавить запись"
      icon="i-lucide-plus"
      variant="outline"
      color="neutral"
      size="sm"
      block
      @click="option = 'create'"
    />
    <template #body>
      <component :is="FormComponent" :item="item" @update="submitItem" />
    </template>
  </UModal>
</template>
