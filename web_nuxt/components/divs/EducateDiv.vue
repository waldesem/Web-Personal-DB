<script setup lang="ts">
import type { Education } from "@/types";

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
const education = ref({} as Education);
const educations = ref<Education[]>([]);

const { refresh, status } = await useLazyAsyncData("educations", async () => {
  educations.value = (await authFetch(
    "/route/items/educations/" + props.candId
  )) as Education[];
});

async function submitEducation(form: Education) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/educations/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  education.value = {} as Education;
  await refresh();
  emit("message", message);
}

async function deleteEducation(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/educations/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    educations.value.splice(idx, 1);
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
      <FormsEducationForm
        :education="education"
        @cancel="education = {}; modal = false"
        @update="submitEducation"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in educations" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Уровень образования'">{{
        item["view"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Название учебного заведения'">{{
        item["institution"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Год окончания'">{{
        item["finished"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Специальность'">{{
        item["specialty"]
      }}</ElementsLabelSlot>
      <template v-if="props.editable" #footer>
        <ElementsNavSimpHoriz
          @delete="deleteEducation(item['id'], idx)"
          @update="
            education = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
