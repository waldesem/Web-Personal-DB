<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { TabsType, MappedCompType } from "@/types";

import CheckDiv from "@/components/divs/items/CheckItem.vue";
import InquiryDiv from "@/components/divs/items/InquiryItem.vue";
import InvestigateDiv from "@/components/divs/items/InvestigateItem.vue";
import PoligrafDiv from "@/components/divs/items/PoligrafItem.vue";

import CheckForm from "@/components/forms/CheckForm.vue";
import InquiryForm from "@/components/forms/InquiryForm.vue";
import InvestigationForm from "@/components/forms/InvestigationForm.vue";
import PoligrafForm from "@/components/forms/PoligrafForm.vue";

const props = defineProps({
  view: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["editable"]);

const mappedComponents = {
  checks: [CheckDiv, CheckForm],
  inquiries: [InquiryDiv, InquiryForm],
  investigations: [InvestigateDiv, InvestigationForm],
  poligrafs: [PoligrafDiv, PoligrafForm],
} as MappedCompType;

const item = ref({} as TabsType);
const items = ref<TabsType[]>([]);
const modal = ref(false);

const { refresh, status } = await useLazyAsyncData(props.view, async () => {
  items.value = (await useFetchAuth(
    `/route/items/${props.view}/${person.value.id}`
  )) as TabsType[];
});

async function submitItem(form: TabsType) {
  modal.value = false;
  status.value = "pending";
  const { message } = (await useFetchAuth(
    `/route/items/${props.view}/${person.value.id}`,
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
  const { message } = (await useFetchAuth(`/route/items/${props.view}/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  status.value = "success";
  if (message == "success") {
    items.value.splice(idx, 1);
  }
  showToast(message);
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
  const { message } = (await useFetchAuth(
    `/route/explorer/files/${props.view}/${person.value.id}`,
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
    <UModal
      v-model:open="modal"
      :ui="{ content: 'sm:max-w-4xl overflow-y-auto' }"
      :dismissible="false"
      title="Проверка кандидата"
      description="Данные профиля"
    >
      <template #content>
        <div class="m-4">
          <component
            :is="mappedComponents[props.view][1]"
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
    <div v-for="(content, index) in items" :key="content.id" class="py-4 ms-2">
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
        <div
          v-for="p in Object.keys(item)"
          :key="p"
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
        <component :is="mappedComponents[props.view][0]" :item="content" />
      </div>
      <USeparator v-if="index != items.length - 1" />
    </div>
  </div>
</template>
