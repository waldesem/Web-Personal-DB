<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Education } from "@/utils/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean

const collapse = ref(false);
const itemId = ref("");
const edit = ref(false);
const education = ref({} as Education);

const { refresh } = await useLazyAsyncData("educations", async () => {
  await anketaState.getItem('educations');
})

async function updateEducation(educationForm: Education) {
closeAction();
  Promise.all([
    await anketaState.updateItem("educations", educationForm),
    await refresh()
  ])
}

async function deleteEducation(index: string) {
  Promise.all([
    await anketaState.deleteItem(index, 'educations'),
    await refresh()
  ])
}

async function cancelOperation() {
  await refresh();
  closeAction();
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="editState"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsEducationForm 
        @cancel="cancelOperation" 
        @submit="updateEducation"
      />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.educations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.educations"
      :key="idx"
      class="p-1"
    >
      <UCard>
        <FormsEducationForm
          v-if="edit && itemId == item['id'].toString()"
          :education="education"
          @cancel="cancelOperation"
          @submit="updateEducation"
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
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
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
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>

