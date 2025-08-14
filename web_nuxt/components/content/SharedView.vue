<script setup lang="ts">
import type { DivsItems, PillsItems } from "@/types";

const { $api } = useNuxtApp();

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

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const item = shallowRef({} as object);
const modal = ref(false);

const { data, status, refresh } = await useAPI<object[]>(
  `/route/${props.view}/${candId.value}`,
  {
    lazy: true,
    server: false,
  }
);

async function submitItem(form: object) {
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
    item.value = {} as object;
    makeToast(message, "Информация успешно обновлена");
  } else {
    makeToast();
  }
}

async function deleteItem(id: string, idx: number) {
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
    data.value?.splice(idx, 1);
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
        @delete="deleteItem(content['id' as keyof typeof content], index)"
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
        item = {} as object;
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
