<script setup lang="ts">
import type { Component } from "vue";
import type { DivsItems, PillsItems } from "@/types";

const AddressItem = defineAsyncComponent(
  () => import("@/components/items/AddressItem.vue")
);
const AffilationItem = defineAsyncComponent(
  () => import("@/components/items/AffilationItem.vue")
);
const ContactItem = defineAsyncComponent(
  () => import("@/components/items/ContactItem.vue")
);
const DocumentItem = defineAsyncComponent(
  () => import("@/components/items/DocumentItem.vue")
);
const EducationItem = defineAsyncComponent(
  () => import("@/components/items/EducationItem.vue")
);
const PreviousItem = defineAsyncComponent(
  () => import("@/components/items/PreviousItem.vue")
);
const StaffItem = defineAsyncComponent(
  () => import("@/components/items/StaffItem.vue")
);
const WorkplaceItem = defineAsyncComponent(
  () => import("@/components/items/WorkplaceItem.vue")
);
const CheckItem = defineAsyncComponent(
  () => import("@/components/items/CheckItem.vue")
);
const InquiryItem = defineAsyncComponent(
  () => import("@/components/items/InquiryItem.vue")
);
const InvestigateItem = defineAsyncComponent(
  () => import("@/components/items/InvestigationItem.vue")
);
const PoligrafItem = defineAsyncComponent(
  () => import("@/components/items/PoligrafItem.vue")
);

const AddressForm = defineAsyncComponent(
  () => import("@/components/forms/AddressForm.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@/components/forms/AffilationForm.vue")
);
const ContactForm = defineAsyncComponent(
  () => import("@/components/forms/ContactForm.vue")
);
const DocumentForm = defineAsyncComponent(
  () => import("@/components/forms/DocumentForm.vue")
);
const EducationForm = defineAsyncComponent(
  () => import("@/components/forms/EducationForm.vue")
);
const PreviousForm = defineAsyncComponent(
  () => import("@/components/forms/PreviousForm.vue")
);
const StaffForm = defineAsyncComponent(
  () => import("@/components/forms/StaffForm.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@/components/forms/WorkplaceForm.vue")
);
const CheckForm = defineAsyncComponent(
  () => import("@/components/forms/CheckForm.vue")
);
const InquiryForm = defineAsyncComponent(
  () => import("@/components/forms/InquiryForm.vue")
);
const InvestigateForm = defineAsyncComponent(
  () => import("@/components/forms/InvestigateForm.vue")
);
const PoligrafForm = defineAsyncComponent(
  () => import("@/components/forms/PoligrafForm.vue")
);

const props = defineProps({
  view: {
    type: String as PropType<PillsItems | DivsItems>,
    required: true,
  },
  rows: {
    type: Number,
    required: true,
  },
});

const mappedContent = {
  addresses: [AddressForm, AddressItem],
  affilations: [AffilationForm, AffilationItem],
  contacts: [ContactForm, ContactItem],
  documents: [DocumentForm, DocumentItem],
  educations: [EducationForm, EducationItem],
  previous: [PreviousForm, PreviousItem],
  staffs: [StaffForm, StaffItem],
  workplaces: [WorkplaceForm, WorkplaceItem],
  checks: [CheckForm, CheckItem],
  inquiries: [InquiryForm, InquiryItem],
  investigations: [InvestigateForm, InvestigateItem],
  poligrafs: [PoligrafForm, PoligrafItem],
} as { [props.view]: [Component, Component] };

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const item = ref({} as object);
const items = ref<object[]>([]);
const modal = ref(false);

const { refresh, status } = await useLazyAsyncData(props.view, async () => {
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
  if (message == "success") {
    item.value = {} as object;
    status.value = "success";
    makeToast(message, "Информация успешно обновлена");
  } else {
    makeToast();
    status.value = "error";
  }
}

async function deleteItem(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  status.value = "pending";
  const { message } = (await fetchAuth(`/route/items/${props.view}/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    makeToast(message, "Информация успешно обновлена");
    items.value.splice(idx, 1);
    status.value = "success";
  } else {
    makeToast();
    status.value = "error";
  }
}
</script>

<template>
  <div v-for="(content, index) in items" :key="index" class="py-4 ms-2">
    <LazyElementsDivMenu
      v-if="editable"
      @change="
        item = content;
        modal = true;
      "
      @delete="deleteItem(content['id' as keyof typeof content], index)"
    />
    <ElementsSkeletonDiv v-if="status === 'pending'" :rows="props.rows" />
    <div v-else>
      <component :is="mappedContent[props.view][1]" :item="content" />
    </div>
    <USeparator v-if="index < items.length - 1" />
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
    title="Данные проверки"
    description="Введите или отредактируйте информацию о проверке"
  >
    <template #body>
      <component
        :is="mappedContent[props.view][0]"
        :item="item"
        @update="submitItem"
      />
    </template>
  </UModal>
</template>
