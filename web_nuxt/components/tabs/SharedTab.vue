<script setup lang="ts">
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
  component: {
    type: String,
    required: true,
  },
});

const mappedComponents = {
  checks: [CheckDiv, CheckForm],
  inquiries: [InquiryDiv, InquiryForm],
  investigations: [InvestigateDiv, InvestigationForm],
  poligrafs: [PoligrafDiv, PoligrafForm],
} as MappedCompType;

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const item = ref({} as TabsType);
const items = ref<TabsType[]>([]);
const modal = ref(false);
const pending = ref(false);

const { refresh, status } = await useLazyAsyncData(props.component, async () => {
  items.value = (await useFetchAuth(
    `/route/items/${props.component}/${candId.value}`
  )) as TabsType[];
});

async function submitItem(form: TabsType) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
    `/route/items/${props.component}/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  item.value = {} as TabsType;
  await refresh();
  emitMessage(message);
}

async function deleteItem(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await useFetchAuth(`/route/items/${props.component}/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    items.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <UCard
    :variant="status == 'pending' || pending ? 'soft' : 'outline'"
    class="my-2 mx-1"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  > 
    <UModal
      v-model:open="modal"
      :ui="{ content: 'sm:max-w-4xl overflow-y-auto' }"
      :dismissible="false"
      title="Проверка кандидата"
      description="Данные профиля"
    >
      <template #content>
        <UCard class="m-2">
          <component
            :is="mappedComponents[props.component][1]"
            :item="item"
            @cancel="
              item = {} as TabsType;
              modal = false;
            "
            @update="submitItem"
          />
        </UCard>
      </template>
    </UModal>
    <UButton
      v-if="editable"
      :loading="status == 'pending' || pending"
      label="Добавить запись"
      variant="ghost"
      icon="i-heroicons-plus-circle"
      @click="modal = !modal"
    />
    <UCard
      v-for="(content, index) in items"
      :key="content.id"
      :variant="status == 'pending' || pending ? 'soft' : 'outline'"
      class="m-2"
    >
      <component :is="mappedComponents[props.component][0]" :item="content" />
      <template v-if="editable" #footer>
        <ElementsTabMenu
          v-if="items.length > 0 && (status != 'pending' || !pending)"
          :item="props.component"
          @cancel="modal = false"
          @delete="deleteItem(content.id, index)"
          @update="
            item = content;
            modal = true;
          "
        />
      </template>
    </UCard>
    <div v-if="!items.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
  </UCard>
</template>
