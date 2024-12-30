<script setup lang="ts">
import type { Contact } from "@/types";

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
const contact = ref({} as Contact);
const contacts = ref<Contact[]>([]);

const { refresh, status } = await useLazyAsyncData("contacts", async () => {
  contacts.value = (await authFetch(
    "/route/items/contacts/" + props.candId
  )) as Contact[];
});

async function submitContact(form: Contact) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/contacts/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  await refresh();
  emit("message", message);
}

async function deleteContact(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/contacts/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    contacts.value.splice(idx, 1);
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
      <FormsContactForm
        :contact="contact"
        @cancel="modal = false"
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
      <template v-if="props.editable" #footer>
        <ElementsNavSimpHoriz
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
