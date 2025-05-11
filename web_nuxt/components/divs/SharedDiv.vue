<script setup lang="ts">
import type { DivsType, MappedCompType } from "@/types";

import AddressItem from "@/components/divs/items/AddressItem.vue";
import AffilItem from "@/components/divs/items/AffilItem.vue";
import ContactItem from "@/components/divs/items/ContactItem.vue";
import DocumItem from "@/components/divs/items/DocumItem.vue";
import EducateItem from "@/components/divs/items/EducateItem.vue";
import PrevItem from "@/components/divs/items/PrevItem.vue";
import StaffItem from "@/components/divs/items/StaffItem.vue";
import WorkItem from "@/components/divs/items/WorkItem.vue";

import AddressForm from "@/components/forms/AddressForm.vue";
import AffilationForm from "@/components/forms/AffilationForm.vue";
import ContactForm from "@/components/forms/ContactForm.vue";
import DocumentForm from "@/components/forms/DocumentForm.vue";
import EducationForm from "@/components/forms/EducationForm.vue";
import PreviousForm from "@/components/forms/PreviousForm.vue";
import StaffForm from "@/components/forms/StaffForm.vue";
import WorkplaceForm from "@/components/forms/WorkplaceForm.vue";

const props = defineProps({
  view: {
    type: String,
    required: true,
  },
});

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const mappedComponents = {
  addresses: [AddressItem, AddressForm],
  affilations: [AffilItem, AffilationForm],
  contacts: [ContactItem, ContactForm],
  documents: [DocumItem, DocumentForm],
  educations: [EducateItem, EducationForm],
  previous: [PrevItem, PreviousForm],
  staffs: [StaffItem, StaffForm],
  workplaces: [WorkItem, WorkplaceForm],
} as MappedCompType;

const item = ref({} as DivsType);
const items = ref([] as DivsType[]);
const modal = ref(false);
const pending = ref(false);

const { refresh, status } = await useLazyAsyncData(props.view, async () => {
  items.value = (await await useFetchAuth(
    `/route/items/${props.view}/${candId.value}`
  )) as DivsType[];
});

async function submitItem(form: DivsType) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
    `/route/items/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  item.value = {} as DivsType;
  await refresh();
  emitMessage(message);
}

async function deleteItem(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await useFetchAuth(`/route/items/${props.view}/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
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
  <div v-for="(itm, idx) in items" :key="idx" class="py-2 ms-2">
    <div class="relative">
      <div class="absolute top-2 right-2">
        <UDropdownMenu
          :disabled="!editable"
          :items="[
            {
              label: 'Изменить',
              icon: 'i-heroicons-pencil-square',
              onSelect() {
                item = items[idx];
                modal = true;
              },
            },
            {
              label: 'Удалить',
              icon: 'i-heroicons-trash',
              onSelect() {
                deleteItem(items[idx].id, idx);
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
    <component :is="mappedComponents[props.view][0]" :item="itm" />
    <USeparator v-if="idx != items.length - 1" />
  </div>
  <UModal
    v-model:open="modal"
    :dismissible="false"
    title="Адреса"
    description="Данные профиля"
  >
    <template #content>
      <div class="p-4">
        <component
          :is="mappedComponents[props.view][1]"
          :item="item"
          @cancel="
            item = {} as DivsType;
            modal = false;
          "
          @update="submitItem"
        />
      </div>
    </template>
  </UModal>
  <div class="py-2 border-t border-gray-200">
    <UButton
      :disabled="!editable"
      label="Добавить запись"
      icon="i-heroicons-document-plus"
      variant="ghost"
      @click="
        item = {} as DivsType;
        modal = true;
      "
    />
  </div>
</template>
