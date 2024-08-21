<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Education } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const itemId = ref("");
const edit = ref(false);
const education = ref({} as Education);

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <div v-if="collapse" class="p-1">
    <div class="border rounded p-3">
      <FormsEducationForm @cancel="cancelAction" />
    </div>
  </div>
  <div v-if="anketaState.anketa.value.educations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.educations"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
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
          <ElementsNaviHorizontal
            v-show="
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['editable']
            "
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'educations')"
            @update="
              education = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>
