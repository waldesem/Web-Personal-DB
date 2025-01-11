<script setup lang="ts">
import type { Needs } from "@/types";
import { emitMessage } from "@/utils";

prefetchComponents("FormsInquiryForm");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const need = ref({} as Needs);
const inquiries = ref<Needs[]>([]);

const { refresh, status } = await useLazyAsyncData("inquiries", async () => {
  inquiries.value = (await authFetch(
    `/route/items/inquiries/${candId.value}`
  )) as Needs[];
});

async function submitIquiry(form: Needs) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/inquiries/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  need.value = {} as Needs;
  await refresh();
  emitMessage(message);
}

async function deleteNeed(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/inquiries/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    inquiries.value.splice(idx, 1);
  }
  emitMessage(message);
}

const items = computed(() =>
  inquiries.value.map((item, _) => ({
    label: "Запрос о сотруднике ID #" + item["id"],
    defaultOpen: true,
    description: item,
  }))
);
</script>

<template>
  <div v-if="editable || status == 'pending'" class="my-1">
    <UButton
      :loading="status == 'pending' || pending"
      :label="
        status == 'pending' || pending
          ? 'Обновление данных...'
          : 'Добавить запись'
      "
      variant="link"
      @click="modal = !modal"
    />
  </div>
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsInquiryForm
        :inquiry="need"
        @cancel="
          need = {} as Needs;
          modal = false;
        "
        @update="submitIquiry"
      />
    </ElementsCardDiv>
  </UModal>
  <UAccordion :items="items" size="lg" multiple>
    <template #item="{ item, index }">
      <ElementsCardDiv>
        <ElementsLabelSlot :label="'Информация'">{{
          item.description.info
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Иннициатор'">{{
          item.description.initiator
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item.description.created).toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
        <template v-if="editable" #footer>
          <ElementsTabMenu
            :item="'inquiries'"
            @delete="deleteNeed(item.description.id, index)"
            @update="
              need = item.description;
              modal = true;
            "
          />
        </template>
      </ElementsCardDiv>
    </template>
  </UAccordion>
</template>
