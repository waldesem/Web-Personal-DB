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
    <div class="relative">
      <div class="absolute top-2 right-2">
        <UDropdownMenu
          :disabled="editable"
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
                deleteItem(item['id' as keyof typeof item], idx);
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
      <ElementsSkeletonDiv :rows=3 />
    </div>
    <div v-else>
      <ItemsSharedItem :view="props.view" :item="itm" />
    </div>
    <USeparator v-if="idx != items.length - 1" icon="i-heroicons-bolt" />
  </div>
  <div v-if="!items.length && status === 'pending'">
    <ElementsSkeletonDiv :rows=3 />
  </div>
  <div class="py-2 border-t border-gray-200">
    <UButton
      :disabled="!editable"
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
      v-if="editable" 
      v-model:open="modal"
      :ui="{ content: 'sm:max-w-4xl' }"
      :dismissible="false"
      title="Данные профиля"
      description="Введите или отредактируйте данные профиля"
    >
      <template #body>
        <div class="m-4">
          <component
            :is="(mappedComponents[props.view] as Component)"
            :item="item"
            @cancel="
              modal = false;
              item = {} as object;
            "
            @update="submitItem"
          />
        </div>
      </template>
    </UModal>
  </div>
</template>
