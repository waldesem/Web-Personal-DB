<script setup lang="ts">
import type { Contact } from "@/types";

await preloadComponents("DivsItemsContactItem");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const contact = ref({} as Contact);
const contacts = ref<Contact[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("contacts", async () => {
  contacts.value = (await useFetchAuth(
    "/route/items/contacts/" + candId.value
  )) as Contact[];
});

async function submitContact(form: Contact) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
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
  const { message } = (await useFetchAuth(`/route/items/contacts/${id}`, {
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
    :variant="status == 'pending' || pending ? 'soft' : 'outline'"
    class="my-2 mx-1"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <div v-for="(item, idx) in contacts" :key="idx" class="p-1">
      <UCard :variant="status == 'pending' || pending ? 'soft' : 'outline'">
        <div class="flex">
          <div v-if="editable" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="contact" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsContactItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <div v-if="!contacts.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
    <template v-if="editable" #footer>
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
        :loading="status == 'pending' || pending"
        @click="
          contact = {} as Contact;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="contacts.length > 0 && (status != 'pending' || !pending)"
        @update="
          contact = contacts[index];
          modal = true;
        "
        @delete="deleteContact(contacts[index].id, index)"
      />
    </template>
  </UCard>
</template>
