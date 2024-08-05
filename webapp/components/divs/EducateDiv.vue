<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/utils/state";
import type { Education } from "@/utils/interfaces";

const actions = ref(false);
const itemId = ref('');
const edit = ref(false);
const education = ref(<Education>{});

function cancelAction(){
  edit.value = false;
  itemId.value = "";
  const collapsePrevious = document.getElementById('educationer');
  collapsePrevious?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <ElementsDropDownHead :id="'educationer'" :header="'Образование'"/>
  <div class="collapse card card-body mb-3" id="educationer">
    <FormsEducationForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.educations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.educations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
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
                stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
                stateAnketa.anketa.persons['standing']
              "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'educations')"
            @update="
              education = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Уровень образования'">{{ item["view"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Название учебного заведения'">{{
          item["institution"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Год окончания'">{{ item["finished"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Специальность'">{{ item["specialty"] }}</ElementsLabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>