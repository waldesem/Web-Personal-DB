<script setup lang="ts">
import type { TabsType, MappedCompType } from "@/types";

import CheckDiv from "@/components/divs/items/CheckItem.vue";
import InquiryDiv from "@/components/divs/items/InquiryItem.vue";
import InvestigateDiv from "@/components/divs/items/InvestigateItem.vue";
import PoligrafDiv from "@/components/divs/items/PoligrafItem.vue";

import CheckForm from "@/components/forms/CheckForm.vue";
import InquiryForm from "@/components/forms/InquiryForm.vue";
import InvestigationForm from "@/components/forms/InvestigationForm.vue";
import PoligrafForm from "@/components/forms/PoligrafForm.vue";

const props = defineProps({
  component: {
    type: String,
    required: true,
  },
});

const mappedComponents = {
  checks: [CheckDiv, CheckForm],
  inquiries: [InquiryDiv, InquiryForm],
  investigations: [InvestigateDiv, InvestigationForm],
  poligrafs: [PoligrafDiv, PoligrafForm],
} as MappedCompType;

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const item = ref({} as TabsType);
const items = ref<TabsType[]>([]);
const modal = ref(false);
const pending = ref(false);

const { refresh, status } = await useLazyAsyncData(
  props.component,
  async () => {
    items.value = (await useFetchAuth(
      `/route/items/${props.component}/${candId.value}`
    )) as TabsType[];
  }
);

async function submitItem(form: TabsType) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
    `/route/items/${props.component}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  item.value = {} as TabsType;
  await refresh();
  emitMessage(message);
}

async function deleteItem(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await useFetchAuth(
    `/route/items/${props.component}/${id}`,
    {
      method: "DELETE",
    }
  )) as Record<string, string>;
  if (message == "success") {
    items.value.splice(idx, 1);
  }
  emitMessage(message);
}

const loading = computed(() => {
  return status.value == "pending" || pending.value;
});
</script>

<template>
  <div class="flex flex-col items-center justify-center">
    <UModal
      v-model:open="loading"
      :dismissible="false"
      title="Load"
      description="Loading data"
    >
      <template #content><UProgress animation="swing" /></template>
    </UModal>
  </div>
  <div class="mt-2">
    <UButton
      v-if="editable"
      class="flex justify-end "
      label="Добавить запись"
      variant="ghost"
      icon="i-heroicons-document-plus"
      @click="modal = !modal"
    />
    <UModal
      v-model:open="modal"
      :ui="{ content: 'sm:max-w-4xl overflow-y-auto' }"
      :dismissible="false"
      title="Проверка кандидата"
      description="Данные профиля"
    >
      <template #content>
        <div class="m-4">
          <component
            :is="mappedComponents[props.component][1]"
            :item="item"
            @cancel="
              item = {} as TabsType;
              modal = false;
            "
            @update="submitItem"
          />
        </div>
      </template>
    </UModal>
    <div v-for="(content, index) in items" :key="content.id" class="py-4 ms-2">
      <div v-if="editable" class="relative">
        <div class="absolute top-2 right-2">
          <ElementsTabMenu
            :item="props.component"
            @delete="deleteItem(content.id, index)"
            @update="
              item = content;
              modal = true;
            "
          />
        </div>
      </div>
      <component :is="mappedComponents[props.component][0]" :item="content" />
      <USeparator v-if="index != items.length - 1" />
    </div>
  </div>
</template>
