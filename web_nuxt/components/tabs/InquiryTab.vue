<script setup lang="ts">
import type { Needs } from "@/types";

prefetchComponents("FormsInquiryForm");

const emit = defineEmits(["message"]);

const authFetch = useFetchAuth();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const modal = ref(false);
const pending = ref(true);
const need = ref({} as Needs);
const inquiries = ref<Needs[]>([]);

const { refresh, status } = await useLazyAsyncData("inquiries", async () => {
  inquiries.value = (await authFetch(
    `/route/items/inquiries/${props.candId}`
  )) as Needs[];
});

async function submitIquiry(form: Needs) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/inquiries/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  await refresh();
  emit("message", message);
}

async function deleteNeed(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/inquiries/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    inquiries.value.splice(idx, 1);
  }
  emit("message", message);
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :loading="status == 'pending' || pending"
    :label="
      status == 'pending' || pending
        ? 'Обновление данных...'
        : 'Добавить запись'
    "
    variant="link"
    @click="modal = !modal"
  />
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsInquiryForm
        :inquiry="need"
        @cancel="modal = false"
        @update="submitIquiry"
      />
    </ElementsCardDiv>
  </UModal>
  <div
    v-for="(item, index) in inquiries"
    :key="index"
    class="text-sm text-gray-500 dark:text-gray-400 py-1"
  >
    <ElementsCardDiv>
      <template #header>
        <div class="tex-base text-red-800 font-medium">
          {{ "Запрос о сотруднике ID #" + item["id"] }}
        </div>
      </template>
      <ElementsLabelSlot v-if="item['info']" :label="'Информация'">{{
        item["info"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['initiator']" :label="'Иннициатор'">{{
        item["initiator"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дата записи'">
        {{ new Date(item["created"]).toLocaleString("ru-RU") }}
      </ElementsLabelSlot>
      <template v-if="props.editable" #footer>
        <ElementsNaviHorizont
          :cand-id="props.candId"
          :item="'inquiries'"
          @delete="deleteNeed(item['id'], index)"
          @update="
            need = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
