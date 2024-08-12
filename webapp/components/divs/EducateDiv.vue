<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Education } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const collapse = ref(false);
const itemId = ref("");
const edit = ref(false);
const education = ref(<Education>{});

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
  <div v-if="collapse" class="border rounded p-3">
    <FormsEducationForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.educations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.educations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="border rounded p-3"
    >
      <FormsEducationForm
        v-if="edit && itemId == item['id'].toString()"
        :education="education"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
              actions &&
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']
            "
            @delete="
              anketaState.deleteItem(item['id'].toString(), 'educations')
            "
            @update="
              education = item;
              itemId = item['id'].toString();
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
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
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>
