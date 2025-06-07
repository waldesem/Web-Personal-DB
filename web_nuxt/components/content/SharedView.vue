<script setup lang="ts">
import type { DivItems, TabItems } from "@/types";

import type { Component } from "vue";
import AddressItem from "@/components/items/AddressItem.vue";
import AffilationItem from "@/components/items/AffilationItem.vue";
import ContactItem from "@/components/items/ContactItem.vue";
import DocumentItem from "@/components/items/DocumentItem.vue";
import EducationItem from "@/components/items/EducationItem.vue";
import PreviousItem from "@/components/items/PreviousItem.vue";
import StaffItem from "@/components/items/StaffItem.vue";
import WorkplaceItem from "@/components/items/WorkplaceItem.vue";
import CheckItem from "@/components/items/CheckItem.vue";
import InquiryItem from "@/components/items/InquiryItem.vue";
import InvestigateItem from "@/components/items/InvestigationItem.vue";
import PoligrafItem from "@/components/items/PoligrafItem.vue";

import AddressForm from "@/components/forms/AddressForm.vue";
import AffilationForm from "@/components/forms/AffilationForm.vue";
import ContactForm from "@/components/forms/ContactForm.vue";
import DocumentForm from "@/components/forms/DocumentForm.vue";
import EducationForm from "@/components/forms/EducationForm.vue";
import PreviousForm from "@/components/forms/PreviousForm.vue";
import StaffForm from "@/components/forms/StaffForm.vue";
import WorkplaceForm from "@/components/forms/WorkplaceForm.vue";
import CheckForm from "@/components/forms/CheckForm.vue";
import InquiryForm from "@/components/forms/InquiryForm.vue";
import InvestigateForm from "@/components/forms/InvestigateForm.vue";
import PoligrafForm from "@/components/forms/PoligrafForm.vue";

const props = defineProps({
  view: {
    type: String as PropType<TabItems | DivItems>,
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
} as { [key in DivItems | TabItems]: Component[] };

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
  status.value = "success";
  item.value = {} as object;
  await refresh();
  if (message == "success") {
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
  status.value = "success";
  if (message == "success") {
    makeToast(message, "Информация успешно обновлена");
    items.value.splice(idx, 1);
  } else makeToast();
}
</script>

<template>
  <div v-for="(content, index) in items" :key="index" class="py-2 ms-2">
    <div v-if="editable" class="relative">
      <div class="absolute right-1">
        <UDropdownMenu
          :items="[
            {
              label: 'Изменить',
              icon: 'i-heroicons-pencil-square',
              onSelect() {
                item = content;
                modal = true;
              },
            },
            {
              label: 'Удалить',
              icon: 'i-heroicons-trash',
              onSelect() {
                deleteItem(content['id' as keyof typeof content], index);
              },
            },
          ]"
          :content="{ align: 'end' }"
        >
          <UButton
            size="xl"
            color="neutral"
            icon="i-heroicons-ellipsis-vertical"
            variant="ghost"
            title="Выбор действия"
          />
        </UDropdownMenu>
      </div>
    </div>
    <ElementsSkeletonDiv v-if="status === 'pending'" :rows="props.rows" />
    <div v-else>
      <component
        :is="(mappedContent[props.view as keyof typeof mappedContent][0] as Component)"
        :item="content"
        @update="submitItem"
      />
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
      icon="i-heroicons-document-plus"
      variant="ghost"
      @click="
        item = {} as object;
        modal = true;
      "
    />
  </div>
  <UModal
    v-model:open="modal"
    :ui="{ content: 'sm:max-w-4xl' }"
    title="Данные проверки"
    description="Введите или отредактируйте информацию о проверке"
  >
    <template #body>
      <component
        :is="(mappedContent[props.view as keyof typeof mappedContent][1] as Component)"
        :item="item"
        @update="submitItem"
      />
    </template>
  </UModal>
</template>
