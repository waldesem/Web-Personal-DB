<script setup lang="ts">
import type { DivsType, MappedType } from "@/types";

import AddressForm from "@/components/forms/AddressForm.vue";
import AffilationForm from "@/components/forms/AffilationForm.vue";
import ContactForm from "@/components/forms/ContactForm.vue";
import DocumentForm from "@/components/forms/DocumentForm.vue";
import EducationForm from "@/components/forms/EducationForm.vue";
import PreviousForm from "@/components/forms/PreviousForm.vue";
import StaffForm from "@/components/forms/StaffForm.vue";
import WorkplaceForm from "@/components/forms/WorkplaceForm.vue";

const emits = defineEmits(["open"]);

const props = defineProps({
  view: {
    type: String,
    required: true,
  },
});

const mappedComponents = {
  addresses: AddressForm,
  affilations: AffilationForm,
  contacts: ContactForm,
  documents: DocumentForm,
  educations: EducationForm,
  previous: PreviousForm,
  staffs: StaffForm,
  workplaces: WorkplaceForm,
} as MappedType;

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const item = ref({} as DivsType);
const items = ref([] as DivsType[]);
const modal = ref(false);

const { refresh, status } = await useLazyAsyncData(props.view, async () => {
  items.value = (await fetchAuth(
    `/route/items/${props.view}/${candId.value}`
  )) as DivsType[];
});

async function submitItem(form: DivsType) {
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
  item.value = {} as DivsType;
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
    items.value.splice(idx, 1);
  }
  if (message == "success") {
    makeToast(message, "Информация успешно удалена");
  } else {
    makeToast();
  }
}
</script>

<template>
  <div v-for="(itm, idx) in items" :key="idx" class="py-2 ms-2">
    <div v-if="editable" class="relative">
      <div class="absolute top-2 right-2">
        <UDropdownMenu
          :items="[
            {
              label: 'Изменить',
              icon: 'i-heroicons-pencil-square',
              onSelect() {
                item = items[idx];
                modal = true;
                emits('open', true);
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
            :loading="status == 'pending'"
            size="xl"
            color="neutral"
            icon="i-heroicons-ellipsis-vertical"
            variant="ghost"
            title="Выбор действия"
          />
        </UDropdownMenu>
      </div>
    </div>
    <div v-if="status === 'pending'">
      <div
        v-for="i in 3"
        :key="i"
        class="flex grid grid-cols-12 gap-3 mb-3"
      >
        <div class="col-span-3">
          <USkeleton class="h-4" />
        </div>
        <div class="col-span-9">
          <USkeleton class="h-4 w-[300px]" />
        </div>
      </div>
    </div>
    <div v-else>
      <ItemsSharedItem :view="props.view" :item="itm" />
    </div>
    <USeparator v-if="idx != items.length - 1" />
  </div>
  <UModal
    v-if="editable" 
    v-model:open="modal"
    :ui="{ content: 'sm:max-w-4xl' }"
    :dismissible="false"
    title="Проверка кандидата"
    description="Данные профиля"
  >
    <template #content>
      <div class="m-4">
        <component
          :is="mappedComponents[props.view]"
          :item="item"
          @cancel="
            modal = false;
            item = {} as DivsType;
          "
          @update="submitItem"
        />
      </div>
    </template>
  </UModal>
  <div class="py-2 border-t border-gray-200">
    <UButton
      :disabled="!editable"
      :loading="status == 'pending'"
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
