<script setup lang="ts">
import type { Work } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

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
const workplace = ref({} as Work);

const {
  data: workplaces,
  refresh,
  status,
} = await useLazyAsyncData("workplaces", async () => {
  const response = await authFetch("/api/workplaces/" + props.candId);
  return response as Work[];
});

async function submitWorkplace(form: Work) {
  pending.value = false;
  closeAction();
  await authFetch("/api/workplaces/" + props.candId, {
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

async function deleteWork(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  authFetch("/api/workplaces/" + id, {
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
      <UCard>
        <FormsWorkplaceForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitWorkplace"
        />
      </UCard>
    </div>
  </Transition>
  <div v-if="workplaces && workplaces.length">
    <div v-for="(item, idx) in workplaces" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
      <UCard v-else>
        <FormsWorkplaceForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :work="workplace"
          @cancel="cancelOperation"
          @update="submitWorkplace"
        />
        <div v-else>
          <ElementsLabelSlot v-if="item['now_work']" :label="'Текущая работа'">
            {{ item["now_work"] ? "Да" : "Нет" }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Начало работы'">
            {{ new Date(item["starts"]).toLocaleDateString("ru-RU") }}
          </ElementsLabelSlot>
          <ElementsLabelSlot
            v-if="!item['now_work']"
            :label="'Окончание работы'"
          >
            {{ new Date(item["finished"]).toLocaleDateString("ru-RU") }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Место работы'">
            {{ item["workplace"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Адрес'">
            {{ item["addresses"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Должность'">
            {{ item["position"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot
            v-if="item['reason']"
            :label="'Причина увольнения'"
          >
            {{ item["reason"] }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deleteWork(item['id'])"
            @update="
              workplace = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
    <p v-else class="text-primary">Данные о работе отсутствуют</p>
  </div>
</template>
