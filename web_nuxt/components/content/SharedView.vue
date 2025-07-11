<script setup lang="ts">
import type { Component } from "vue";
import type { DivsItems, PillsItems } from "@/types";

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

const mappedContent = {
  addresses: [
    () => import("@/components/forms/AddressForm.vue"),
    () => import("@/components/items/AddressItem.vue"),
  ],
  affilations: [
    () => import("@/components/forms/AffilationForm.vue"),
    () => import("@/components/items/AffilationItem.vue"),
  ],
  contacts: [
    () => import("@/components/forms/ContactForm.vue"),
    () => import("@/components/items/ContactItem.vue"),
  ],
  documents: [
    () => import("@/components/forms/DocumentForm.vue"),
    () => import("@/components/items/DocumentItem.vue"),
  ],
  educations: [
    () => import("@/components/forms/EducationForm.vue"),
    () => import("@/components/items/EducationItem.vue"),
  ],
  previous: [
    () => import("@/components/forms/PreviousForm.vue"),
    () => import("@/components/items/PreviousItem.vue"),
  ],
  staffs: [
    () => import("@/components/forms/StaffForm.vue"),
    () => import("@/components/items/StaffItem.vue"),
  ],
  workplaces: [
    () => import("@/components/forms/WorkplaceForm.vue"),
    () => import("@/components/items/WorkplaceItem.vue"),
  ],
  checks: [
    () => import("@/components/forms/CheckForm.vue"),
    () => import("@/components/items/CheckItem.vue"),
  ],
  inquiries: [
    () => import("@/components/forms/InquiryForm.vue"),
    () => import("@/components/items/InquiryItem.vue"),
  ],
  investigations: [
    () => import("@/components/forms/InquestForm.vue"),
    () => import("@/components/items/InquestItem.vue"),
  ],
  poligrafs: [
    () => import("@/components/forms/PoligrafForm.vue"),
    () => import("@/components/items/PoligrafItem.vue"),
  ],
} as { [props.view]: [Component, Component] };

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const item = ref({} as object);
const items = ref([] as object[]);
const modal = ref(false);

const { status, refresh } = await useLazyAsyncData(props.view, async () => {
  items.value = (await fetchAuth(
    `/route/items/${props.view}/${candId.value}`
  )) as object[];
});

async function submitItem(form: object) {
  modal.value = false;
  status.value = "pending";
  const { message } = (await fetchAuth(
    `/route/items/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
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
  const { message } = (await fetchAuth(`/route/items/${props.view}/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  status.value = message as "success" | "error";
  if (message == "success") {
    makeToast(message, "Информация успешно обновлена");
    items.value.splice(idx, 1);
  } else {
    makeToast();
  }
}
</script>

<template>
  <div v-if="status === 'pending'">
    <div v-for="i in items.length + 1" :key="i">
      <LazyElementsSkeletonDiv :rows="props.rows" />
      <USeparator v-if="i < items.length" />
    </div>
  </div>
  <div v-else>
    <div v-for="(content, index) in items" :key="index" class="py-4 ms-2">
      <LazyElementsDivMenu
        v-if="editable"
        @change="
          item = content;
          modal = true;
        "
        @delete="deleteItem(content['id' as keyof typeof content], index)"
      />
      <LazyElementsWrapperDiv>
        <component :is="mappedContent[props.view][1]" :item="content" />
      </LazyElementsWrapperDiv>
      <USeparator v-if="index < items.length - 1" />
    </div>
    <div v-if="!items.length" class="p-2 text-red-800">Данные отсутствуют</div>
  </div>
  <div
    v-if="editable"
    class="flex justify-start py-2"
    :class="{ 'border-t border-gray-200': items.length > 0 }"
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
        <component
          :is="mappedContent[props.view][0]"
          :item="item"
          @update="submitItem"
        />
      </LazyElementsWrapperDiv>
    </template>
  </UModal>
</template>
