<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
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

const education = ref({
  itemId: "",
  item: <Education>{},
  showActions: false,
});

function cancelAction(){
  education.value.itemId = "";
  Object.keys(education.value.item).forEach(
    (key) => delete education.value.item[key as keyof typeof education.value.item]
  );
  const collapsePrevious = document.getElementById('education');
  collapsePrevious?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <DropDownHead :id="'education'" :header="'Образование'"/>
  <div class="collapse card card-body mb-3" id="education">
    <EducationForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.educations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.educations"
      :key="idx"
      @mouseover="education.showActions = true"
      @mouseout="education.showActions = false"
      class="card card-body mb-3"
    >
      <EducationForm
        v-if="education.itemId === item['id'].toString()"
        :education="education.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="education.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'educations')"
            @update="
              education.item = item;
              education.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Вид образования'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Название учебного заведения'">{{
          item["name"]
        }}</LabelSlot>
        <LabelSlot :label="'Год окончания'">{{ item["finished"] }}</LabelSlot>
        <LabelSlot :label="'Специальность'">{{ item["speciality"] }}</LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
