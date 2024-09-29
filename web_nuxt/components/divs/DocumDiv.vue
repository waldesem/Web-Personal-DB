<script setup lang="ts">
import type { Document } from "@/types/interfaces";

prefetchComponents(['FormsDocumentForm', 'ElementsSkeletonDiv']);

const authFetch = useFetchAuth();

const toast = useToast();

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

const collapse = ref(false);
const pending = ref(false);
const itemId = ref("");
const edit = ref(false);
const doc = ref({} as Document);

const {
  data: documents,
  refresh,
  status,
} = await useLazyAsyncData("documents", async () => {
  const response = await authFetch("/api/documents/" + props.candId);
  return response as Document[];
});

async function submitDocument(form: Document) {
  pending.value = true;
  closeAction();
  await authFetch("/api/documents/" + props.candId, {
    method: "POST",
    body: form,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  pending.value = false;
  refresh();
}

async function deleteDocument(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  await authFetch("/api/documents/" + id, {
    method: "DELETE",
  });
  toast.add({
    icon: "i-heroicons-information-circle",
    title: "Информация",
    description: `Запись с ID ${id} удалена`,
    color: "primary",
  });
  refresh();
}

async function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsDocumentForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitDocument"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="documents && documents.length">
    <div v-for="(item, idx) in documents" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
      <ElementsCardDiv v-else>
        <FormsDocumentForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :docs="doc"
          @cancel="cancelOperation"
          @update="submitDocument"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Вид документа'">{{
            item["view"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Номер документа'">{{
            item["digits"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Серия документа'">{{
            item["series"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата выдачи'">
            {{
              item["issue"]
                ? new Date(String(item["issue"])).toLocaleDateString("ru-RU")
                : ""
            }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Кем выдан'">{{
            item["agency"]
          }}</ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deleteDocument(item['id'])"
            @update="
              doc = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
