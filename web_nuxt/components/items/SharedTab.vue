<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { MappedType } from "@/types";

import CheckForm from "@/components/forms/CheckForm.vue";
import InquiryForm from "@/components/forms/InquiryForm.vue";
import InvestigateForm from "@/components/forms/InvestigateForm.vue";
import PoligrafForm from "@/components/forms/PoligrafForm.vue";
import type { Component } from "vue";

const props = defineProps({
  view: {
    type: String,
    required: true,
  },
  rows: {
    type: Number,
    required: true,
  },
});

const mappedComponents = {
  checks: CheckForm,
  inquiries: InquiryForm,
  investigations: InvestigateForm,
  poligrafs: PoligrafForm,
} as MappedType;

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
    `/route/anketa/files/${props.view}/${candId.value}`,
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
      label="Добавить запись"
      variant="ghost"
      icon="i-heroicons-document-plus"
      @click="modal = true"
    />
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
      <div v-if="status === 'pending'">
        <ElementsSkeletonDiv :rows="props.rows" />
      </div>
      <div v-else>
        <ItemsSharedItem :view="props.view" :item="content" />
      </div>
      <USeparator v-if="index != (items.length - 1)" icon="i-heroicons-bolt" />
    </div>
    <div v-if="!items.length && status === 'pending'">
      <ElementsSkeletonDiv :rows="props.rows" />
    </div>
    <UModal
      v-model:open="modal"
      :ui="{ content: 'sm:max-w-4xl' }"
      title="Данные проверки"
      description="Введите или отредактируйте информацию о проверке"
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
