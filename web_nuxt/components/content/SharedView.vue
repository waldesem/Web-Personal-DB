<script setup lang="ts">
import type { DivsItems, PillsItems } from "@/types";

// Импортируем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  view: {
    type: String as PropType<PillsItems | DivsItems>,
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
const item = shallowRef({} as object);
const data = shallowRef([] as typeof item.value[]);
const modal = ref(false);

// Определяем функцию для получения данных из API
const { status, refresh } = await useLazyAsyncData(async () => {
  data.value = await $api(`/route/${props.view}/${candId.value}`);
});

// Определяем функцию для отправки данных формы на сервер
async function submitItem(form: typeof item.value) {
  modal.value = false;
  status.value = "pending";
  const { message } = await $api<Record<string, string>>(
    `/route/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  );
  await refresh();
  status.value = message as "success" | "error";
  if (message == "success") {
    item.value = {};
    makeToast(message, "Информация успешно обновлена");
  } else {
    makeToast();
  }
}

// Определяем функцию для удаления данных
async function deleteItem(id: string) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  status.value = "pending";
  const { message } = await $api<Record<string, string>>(
    `/route/${props.view}/${id}`,
    {
      method: "DELETE",
    }
  );
  status.value = message as "success" | "error";
  if (message == "success") {
    makeToast(message, "Информация успешно обновлена");
    await refresh();
  } else {
    makeToast();
  }
}
</script>

<template>
  <div v-if="status === 'pending' && data">
    <div v-for="i in data.length + 1" :key="i">
      <LazyElementsSkeletonDiv :rows="props.rows" />
      <USeparator v-if="i < data.length" />
    </div>
  </div>
  <div v-else>
    <div v-for="(content, index) in data" :key="index" class="py-4 ms-2">
      <LazyElementsDivMenu
        v-if="editable"
        @change="
          item = content;
          modal = true;
        "
        @delete="deleteItem(content['id' as keyof typeof content])"
      />
      <LazyElementsWrapperDiv>
        <slot name="item" :item-content="content" />
      </LazyElementsWrapperDiv>
      <USeparator v-if="data && index < data.length - 1" />
    </div>
    <div v-if="!data || !data.length" class="p-2 text-red-800">
      Данные отсутствуют
    </div>
  </div>
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
      @click="
        item = {};
        modal = true;
      "
    />
  </div>
  <UModal
    v-if="editable"
    v-model:open="modal"
    title="Данные профиля"
    description="Введите или отредактируйте данные"
  >
    <template #body>
      <LazyElementsWrapperDiv>
        <slot name="form" :form-content="item" :submit-item="submitItem" />
      </LazyElementsWrapperDiv>
    </template>
  </UModal>
</template>
