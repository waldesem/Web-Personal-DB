<script setup lang="ts">
import type { Inquisition } from "@/types/interfaces";

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
const edit = ref(false);
const itemId = ref("");
const inquisition = ref({} as Inquisition);

const {
  data: investigations,
  refresh,
  status,
} = await useLazyAsyncData("investigations", async () => {
  const response = await authFetch("/api/investigations/" + props.candId);
  return response as Inquisition[];
});

async function submitInvestigations(form: Inquisition) {
  pending.value = true;
  closeAction();
  await authFetch("/api/investigations/" + props.candId, {
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

async function deleteInquisition(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  await authFetch(`/api/investigations/${id}`, {
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
    class="py-3"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsInvestigationForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitInvestigations"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="investigations && investigations.length">
    <div
      v-for="(item, index) in investigations"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="4" />
      <ElementsCardDiv v-else>
        <template #header>
          <div class="tex-base text-red-800 font-medium">
            {{ "Расследование/проверка ID #" + item["id"] }}
          </div>
        </template>
        <FormsInvestigationForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :investigation="item"
          @cancel="cancelOperation"
          @update="submitInvestigations"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тема проверки'">{{
            item["theme"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Информация'">{{
            item["info"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            item["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :cand-id="props.candId"
            :input-id="'investigations-file'"
            :item="'investigations'"
            @update="
              inquisition = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @delete="deleteInquisition(item['id'])"
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="4" />
    <p v-else class="text-red-800">Расследования/Проверки не проводились</p>
  </div>
</template>
