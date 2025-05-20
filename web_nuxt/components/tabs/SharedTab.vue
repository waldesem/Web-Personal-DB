<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { TabsType, MappedType } from "@/types";

import CheckForm from "@/components/forms/CheckForm.vue";
import InquiryForm from "@/components/forms/InquiryForm.vue";
import InvestigationForm from "@/components/forms/InvestigationForm.vue";
import PoligrafForm from "@/components/forms/PoligrafForm.vue";

const props = defineProps({
  view: {
    type: String,
    required: true,
  },
  rows: {
    type: Number,
    required: true,
  }
});

const emit = defineEmits(["editable"]);

const mappedComponents = {
  checks: CheckForm,
  inquiries: InquiryForm,
  investigations: InvestigationForm,
  poligrafs: PoligrafForm,
} as MappedType;

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const item = ref({} as TabsType);
const items = ref<TabsType[]>([]);
const modal = ref(false);

const { refresh, status } = await useLazyAsyncData(props.view, async () => {
  items.value = (await fetchAuth(
    `/route/items/${props.view}/${candId.value}`
  )) as TabsType[];
});

async function submitItem(form: TabsType) {
  modal.value = false;
  status.value = "pending";
  const { message } = (await fetchAuth(
    `/route/items/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  item.value = {} as TabsType;
  if (message == "success") {
    emit("editable");
    makeToast(message, "Информация успешно обновлена");
  } else {
    makeToast();
  }
  await refresh();
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

const { open, reset, onCancel, onChange } = useFileDialog();

onChange(async (files) => {
  if (!files) return;
  const formData = new FormData();
  for (const file of files) {
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      makeToast("info", "Размер одного файла не должен превышать 10 МБ");
      continue;
    }
    formData.append("file", file);
  }
  const { message } = (await fetchAuth(
    `/route/explorer/files/${props.view}/${candId.value}`,
    {
      method: "POST",
      body: formData,
    }
  )) as Record<string, string>;
  if (message == "success") {
    makeToast("success", "Файлы успешно загружены");
  } else {
    makeToast();
  }
  reset();
});

onCancel(() => {
  reset();
});
</script>

<template>
  <div class="mt-2">
    <UButton
      v-if="editable"
      :loading="status == 'pending'"
      class="flex justify-end"
      label="Добавить запись"
      variant="ghost"
      icon="i-heroicons-document-plus"
      @click="modal = !modal"
    />
    <div v-for="(content, index) in items" :key="content.id" class="py-4 ms-2">
      <div class="relative">
        <div class="absolute top-2 right-2">
          <UDropdownMenu
            :disabled="editable"
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
                label: 'Загрузить',
                icon: 'i-heroicons-cloud-arrow-up',
                onSelect() {
                  open();
                },
              },
              {
                label: 'Удалить',
                icon: 'i-heroicons-trash',
                onSelect() {
                  deleteItem(content.id, index);
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
      <div v-if="status === 'pending'">
        <ElementsSkeletonDiv :rows=props.rows />
      </div>
      <div v-else>
        <ItemsSharedItem :view="props.view" :item="content" />
      </div>
      <USeparator v-if="index != items.length - 1" />
    </div>
    <div v-if="!items.length && status === 'pending'">
      <ElementsSkeletonDiv :rows=props.rows />
    </div>
    <UModal
      v-if="editable"
      v-model:open="modal"
      :ui="{ content: 'sm:max-w-4xl' }"
      :dismissible="false"
      title="Проверка кандидата"
      description="Данные проверки"
    >
      <template #content>
        <div class="m-4">
          <component
            :is="mappedComponents[props.view]"
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
  </div>
</template>
