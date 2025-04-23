<script setup lang="ts">
import type { Passport } from "@/types";

await preloadComponents("DivsItemsDocumItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const doc = ref({} as Passport);
const documents = ref<Passport[]>([]);

const { refresh, status } = await useLazyAsyncData("documents", async () => {
  documents.value = (await authFetch(
    "/route/items/documents/" + candId.value
  )) as Passport[];
});

async function submitDocument(form: Passport) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/documents/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  doc.value = {} as Passport;
  await refresh();
  emitMessage(message);
}

async function deleteDocument(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/documents/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  if (message == "success") {
    documents.value.splice(idx, 1);
  }
  emitMessage(message);
}
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
      variant="ghost"
      icon="i-heroicons-plus-circle"
      @click="modal = !modal"
    />
  </div>
  <UModal
    v-model:open="modal"
    :dismissible="false"
    title="Документ"
    description="Данные профиля"
  >
    <template #content>
      <ElementsCardDiv>
        <FormsDocumentForm
          :docs="doc"
          @cancel="
            doc = {} as Passport;
            modal = false;
          "
          @update="submitDocument"
        />
      </ElementsCardDiv>
    </template>
  </UModal>
  <div v-for="(item, idx) in documents" :key="idx" class="p-1">
    <ElementsCardDiv>
      <DivsItemsDocumItem :item="item" />
      <template v-if="editable" #footer>
        <ElementsDivMenu
          @delete="deleteDocument(item.id, idx)"
          @update="
            doc = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
