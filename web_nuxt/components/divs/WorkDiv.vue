<script setup lang="ts">
import type { Work } from "@/types";

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
const pending = ref(false);
const workplace = ref({} as Work);
const workplaces = ref<Work[]>([]);

const { refresh, status } = await useLazyAsyncData("workplaces", async () => {
  workplaces.value = (await authFetch(
    "/route/items/workplaces/" + props.candId
  )) as Work[];
});

async function submitWorkplace(form: Work) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/workplaces/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  workplace.value = {} as Work;
  await refresh();
  emit("message", message);
}

async function deleteWork(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/workplaces/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    workplaces.value.splice(idx, 1);
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
      <FormsWorkplaceForm
        :work="workplace"
        @cancel="workplace = {}; modal = false"
        @update="submitWorkplace"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in workplaces" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot v-if="item['now_work']" :label="'Текущая работа'">
        {{ item["now_work"] ? "Да" : "Нет" }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['starts']" :label="'Начало работы'">
        {{ new Date(item["starts"]).toLocaleDateString("ru-RU").split(",")[0] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['finished']" :label="'Окончание работы'">
        {{
          new Date(item["finished"]).toLocaleDateString("ru-RU").split(",")[0]
        }}
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
      <ElementsLabelSlot v-if="item['reason']" :label="'Причина увольнения'">
        {{ item["reason"] }}
      </ElementsLabelSlot>
      <template v-if="props.editable" #footer>
        <ElementsNavSimpHoriz
          @delete="deleteWork(item['id'], idx)"
          @update="
            workplace = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
