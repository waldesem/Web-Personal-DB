<script setup lang="ts">
import type { Component } from "vue";
import type { DivsItems, PillsItems } from "@/types";

import AddressForm from "@/components/forms/AddressForm.vue";
import AddressItem from "@/components/items/AddressItem.vue";
import AffilationForm from "@/components/forms/AffilationForm.vue";
import AffilationItem from "@/components/items/AffilationItem.vue";
import ContactForm from "@/components/forms/ContactForm.vue";
import ContactItem from "@/components/items/ContactItem.vue";
import DocumentForm from "@/components/forms/DocumentForm.vue";
import DocumentItem from "@/components/items/DocumentItem.vue";
import EducationForm from "@/components/forms/EducationForm.vue";
import EducationItem from "@/components/items/EducationItem.vue";
import PreviousForm from "@/components/forms/PreviousForm.vue";
import PreviousItem from "@/components/items/PreviousItem.vue";
import StaffForm from "@/components/forms/StaffForm.vue";
import StaffItem from "@/components/items/StaffItem.vue";
import WorkplaceForm from "@/components/forms/WorkplaceForm.vue";
import WorkplaceItem from "@/components/items/WorkplaceItem.vue";
import CheckForm from "@/components/forms/CheckForm.vue";
import CheckItem from "@/components/items/CheckItem.vue";
import InquiryForm from "@/components/forms/InquiryForm.vue";
import InquiryItem from "@/components/items/InquiryItem.vue";
import InquestForm from "@/components/forms/InquestForm.vue";
import InquestItem from "@/components/items/InquestItem.vue";
import PoligrafForm from "@/components/forms/PoligrafForm.vue";
import PoligrafItem from "@/components/items/PoligrafItem.vue";

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
  investigations: [InquestForm, InquestItem],
  poligrafs: [PoligrafForm, PoligrafItem],
} as { [props.view]: [Component, Component] };

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const item = ref({} as object);
const modal = ref(false);

const { data, status, refresh } = await useAPI<object[]>(
  `/route/${props.view}/${candId.value}`, {
  lazy: true,
  server: false,
});

async function submitItem(form: object) {
  modal.value = false;
  status.value = "pending";
  const { message } = (await $api<Record<string, string>>(
    `/route/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  ));
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
  const { message } = (await $api<Record<string, string>>(`/route/${props.view}/${id}/${candId.value}`, {
    method: "DELETE",
  }));
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
        <component :is="mappedContent[props.view][1]" :item="content" />
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
        <component
          :is="mappedContent[props.view][0]"
          :item="item"
          @update="submitItem"
        />
      </LazyElementsWrapperDiv>
    </template>
  </UModal>
</template>
