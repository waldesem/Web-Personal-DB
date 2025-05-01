<script setup lang="ts">
import type { Passport } from "@/types";

await preloadComponents("DivsItemsDocumItem");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const doc = ref({} as Passport);
const documents = ref<Passport[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("documents", async () => {
  documents.value = (await useFetchAuth(
    "/route/items/documents/" + candId.value
  )) as Passport[];
});

async function submitDocument(form: Passport) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
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
  const { message } = (await useFetchAuth(`/route/items/documents/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  index.value = 0;
  if (message == "success") {
    documents.value.splice(idx, 1);
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
    <div v-for="(item, idx) in documents" :key="idx" class="p-1">
      <UCard :variant="status == 'pending' || pending ? 'soft' : 'outline'">
        <div class="flex">
          <div v-if="editable" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="document" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsDocumItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <div v-if="!documents.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
    <template v-if="editable" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Документы"
        description="Данные профиля"
      >
        <template #content>
          <UCard>
            <FormsDocumentForm
              :document="doc"
              @cancel="
                doc = {} as Passport;
                modal = false;
              "
              @update="submitDocument"
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
          doc = {} as Passport;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="documents.length > 0 && (status != 'pending' || !pending)"
        @update="
          doc = documents[index];
          modal = true;
        "
        @delete="deleteDocument(documents[index].id, index)"
      />
    </template>
  </UCard>
</template>
