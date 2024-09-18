<script setup lang="ts">
import type { Education } from "@/types/interfaces";

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
const itemId = ref("");
const edit = ref(false);
const education = ref({} as Education);

const {
  data: educations,
  refresh,
  status,
} = await useLazyAsyncData("educations", async () => {
  const response = await authFetch("/api/educations/" + props.candId);
  return response;
});

async function deleteEducation(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const response = await authFetch("/api/educations/" + id, {
    method: "DELETE",
  });
  console.log(response);
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
        <FormsEducationForm @cancel="cancelOperation" @update="refresh" />
      </UCard>
    </div>
  </Transition>
  <div v-if="educations && educations.length">
    <div v-for="(item, idx) in educations" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending'" :rows="8" />
      <UCard v-else>
        <FormsEducationForm
          v-if="edit && itemId == item['id'].toString()"
          :education="education"
          @cancel="cancelOperation"
          @update="refresh"
        />
        <div v-else>
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
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deleteEducation(item['id'])"
            @update="
              education = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending'" :rows="8" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
