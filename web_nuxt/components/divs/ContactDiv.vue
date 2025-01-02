<script setup lang="ts">
import type { Contact } from "@/types";
import { emitMessage } from "@/utils";

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
  <UButton
    v-if="editable"
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
      <FormsContactForm
        :contact="contact"
        @cancel="
          contact = {} as Contact;
          modal = false;
        "
        @update="submitContact"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in contacts" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Вид'">{{ item["view"] }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Контакт'">{{
        item["contact"]
      }}</ElementsLabelSlot>
      <template v-if="editable" #footer>
        <DivMenu
          @delete="deleteContact(item['id'], idx)"
          @update="
            contact = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
