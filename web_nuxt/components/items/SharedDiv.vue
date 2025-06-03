<script setup lang="ts">
import type { MappedType } from "@/types";

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

const item = ref({} as object);
const items = ref([] as object[]);
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
    items.value.splice(idx, 1);
    makeToast(message, "Информация успешно удалена");
  } else {
    makeToast();
  }
}
</script>

<template>
  <div v-for="(content, index) in items" :key="index" class="py-2 ms-2">
    <div v-if="editable" class="relative">
      <div class="absolute top-2 right-2">
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
      <ElementsSkeletonDiv :rows="3" />
    </div>
    <div v-else>
      <ItemsSharedItem :view="props.view" :item="content" />
    </div>
    <USeparator v-if="index != (items.length - 1)" icon="i-heroicons-bolt" />
  </div>
  <div v-if="!items.length && status === 'pending'">
    <ElementsSkeletonDiv :rows="3" />
  </div>
  <div v-if="editable" class="py-2 border-t border-gray-200">
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
    <UModal
      v-model:open="modal"
      :ui="{ content: 'sm:max-w-4xl' }"
      title="Данные профиля"
      description="Введите или отредактируйте данные профиля"
    >
      <template #body>
        <component
          :is="(mappedComponents[props.view] as Component)"
          :item="item"
          @update="submitItem"
        />
      </template>
    </UModal>
  </div>
</template>
