<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Education } from "@/utils/interfaces";

const anketaState = stateAnketa();

const collapse = ref(false);
const itemId = ref("");
const edit = ref(false);
const education = ref({} as Education);

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}

const editState = inject("editState") as boolean
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
        <FormsEducationForm @cancel="cancelAction" />
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
          @cancel="cancelAction"
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
          <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'educations')"
            @update="
              education = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </div>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>

