<script setup lang="ts">
import type { Contact } from "@/types/interfaces";

prefetchComponents(['FormsContactForm', 'ElementsSkeletonDiv']);

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
const contact = ref({} as Contact);

const {
  data: contacts,
  refresh,
  status,
} = await useLazyAsyncData("contacts", async () => {
  const response = await authFetch("/api/contacts/" + props.candId);
  return response as Contact[];
});

async function submitContact(form: Contact) {
  pending.value = true;
  closeAction();
  await authFetch("/api/contacts/" + props.candId, {
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

async function deleteContact(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  await authFetch("/api/contacts/" + id, {
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
        <FormsContactForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitContact"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="contacts && contacts.length">
    <div v-for="(item, idx) in contacts" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
      <ElementsCardDiv v-else>
        <FormsContactForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :contact="contact"
          @cancel="cancelOperation"
          @update="submitContact"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Вид'">{{
            item["view"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Контакт'">{{
            item["contact"]
          }}</ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deleteContact(item['id'])"
            @update="
              contact = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="2" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
