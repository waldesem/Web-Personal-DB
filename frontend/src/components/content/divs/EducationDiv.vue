<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa, stateUser, stateClassify } from "@/state";
import { Education } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const EducationForm = defineAsyncComponent(
  () => import("@components/content/forms/EducationForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

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
  <DropDownHead :id="'educationer'" :header="'Образование'"/>
  <div class="collapse card card-body mb-3" id="educationer">
    <EducationForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.educations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.educations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <EducationForm
        v-if="edit && itemId == item['id'].toString()" 
        :education="education"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="
                actions &&
                stateAnketa.anketa.persons['user_id'] == stateUser.userId &&
                stateAnketa.anketa.persons['standing'] ==
                  stateClassify.standing['manual']
              "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'educations')"
            @update="
              education = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Уровень образования'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Название учебного заведения'">{{
          item["institution"]
        }}</LabelSlot>
        <LabelSlot :label="'Год окончания'">{{ item["finished"] }}</LabelSlot>
        <LabelSlot :label="'Специальность'">{{ item["speciality"] }}</LabelSlot>
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