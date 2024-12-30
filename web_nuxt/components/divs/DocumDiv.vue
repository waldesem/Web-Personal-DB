<script setup lang="ts">
import type { Document } from "@/types";

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
const doc = ref({} as Document);
const documents = ref<Document[]>([]);

const { refresh, status } = await useLazyAsyncData("documents", async () => {
  documents.value = (await authFetch(
    "/route/items/documents/" + props.candId
  )) as Document[];
});

async function submitDocument(form: Document) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/documents/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  await refresh();
  emit("message", message);
}

async function deleteDocument(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/documents/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    documents.value.splice(idx, 1);
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
      <FormsDocumentForm
        :document="doc"
        @cancel="modal = false"
        @update="submitDocument"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in documents" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Вид документа'">{{
        item["view"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Серия документа'">{{
        item["series"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Номер документа'">{{
        item["digits"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['issue']" :label="'Дата выдачи'">
        {{ new Date(item["issue"]).toLocaleDateString("ru-RU").split(",")[0] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Кем выдан'">{{
        item["agency"]
      }}</ElementsLabelSlot>
      <template v-if="props.editable" #footer>
        <ElementsNavSimpHoriz
          @delete="deleteDocument(item['id'], idx)"
          @update="
            doc = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
