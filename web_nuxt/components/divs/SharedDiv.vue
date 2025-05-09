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
const index = ref(0);

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
  index.value = 0;
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
    <div v-for="(itm, idx) in items" :key="idx" class="p-1">
      <UCard :variant="status == 'pending' || pending ? 'soft' : 'outline'">
        <div class="flex">
          <div v-if="editable" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="item" :value="idx" >
          </div>
          <div class="flex-grow">
            <component :is="mappedComponents[props.view][0]" :item="itm" />
          </div>
        </div>
      </UCard>
    </div>
    <div v-if="!items.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
    <template v-if="editable" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Адреса"
        description="Данные профиля"
      >
        <template #content>
          <UCard class="m-2">
            <component
              :is="mappedComponents[props.view][1]"
              :item="item"
              @cancel="
                item = {} as DivsType;
                modal = false;
              "
              @update="submitItem"
            />
          </UCard>
        </template>
      </UModal>
      <UButton
        icon="i-heroicons-document-plus"
        label="Добавить"
        variant="ghost"
        :loading="status == 'pending' || pending"
        @click="
          item = {} as DivsType;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="items.length > 0 && (status != 'pending' || !pending)"
        @update="
          item = items[index];
          modal = true;
        "
        @delete="deleteItem(items[index].id, index)"
      />
    </template>
  </UCard>
</template>
