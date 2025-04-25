<script setup lang="ts">
import type { Contact } from "@/types";

await preloadComponents("DivsItemsContactItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const contact = ref({} as Contact);
const contacts = ref<Contact[]>([]);
const index = ref(0);

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
  index.value = 0;
  if (message == "success") {
    contacts.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <UCard
    class="m-2"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <USwitch
      v-if="editable"
      v-model="edit"
      :label="edit ? 'Отключить редактирование' : 'Включить редактирование'"
      size="xs"
      class="mb-2 me-2 justify-end"
    />
    <div v-for="(item, idx) in contacts" :key="idx" class="p-1">
      <UCard>
        <div class="flex">
          <div v-if="edit" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="contact" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsContactItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <template v-if="edit" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Контакты"
        description="Данные профиля"
      >
        <template #content>
          <UCard>
            <FormsContactForm
              :contact="contact"
              @cancel="
                contact = {} as Contact;
                modal = false;
              "
              @update="submitContact"
            />
          </UCard>
        </template>
      </UModal>
      <UButton
        icon="i-heroicons-document-plus"
        label="Добавить"
        variant="ghost"
        @click="
          contact = {} as Contact;
          modal = true;
        "
      />
      <ElementsDivMenu
        @update="
          contact = contacts[index];
          modal = true;
        "
        @delete="deleteContact(contacts[index].id, index)"
      />
    </template>
  </UCard>
</template>
