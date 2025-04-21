<script setup lang="ts">
import type { Contact } from "@/types";

await preloadComponents("DivsItemsContactItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const contact = ref({} as Contact);
const contacts = ref<Contact[]>([]);

const { refresh, status } = await useLazyAsyncData("contacts", async () => {
  contacts.value = (await authFetch(
    "/route/items/contacts/" + candId.value
  )) as Contact[];
});

async function submitContact(form: Contact) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/contacts/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  contact.value = {} as Contact;
  await refresh();
  emitMessage(message);
}

async function deleteContact(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/contacts/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  if (message == "success") {
    contacts.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
    <ElementsCardDiv>
    <div class="flex justify-between items-center mx-2">
      <div class="flex items-center space-x-2">
        <UIcon name="i-heroicons-phone" class="size-5" />
        <div class="font-bold">Контакты</div>
      </div>
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
    </div>
  <UModal
    v-model:open="modal"
    :dismissible="false"
    title="Контакты"
    description="Данные профиля"
  >
    <template #content>
      <ElementsCardDiv>
        <FormsContactForm
          :contact="contact"
          @cancel="
            contact = {} as Contact;
            modal = false;
          "
          @update="submitContact"
        />
      </ElementsCardDiv>
    </template>
  </UModal>
  <div v-for="(item, idx) in contacts" :key="idx" class="p-1">
    <ElementsCardDiv>
      <DivsItemsContactItem :item="item" />
      <template v-if="editable" #footer>
        <ElementsDivMenu
          @delete="deleteContact(item.id, idx)"
          @update="
            contact = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
  </ElementsCardDiv>
</template>
