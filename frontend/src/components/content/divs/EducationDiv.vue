<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Education } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
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

onBeforeMount(async () => {
  await stateAnketa.getItem("education");
});

const education = ref({
  action: "",
  itemId: "",
  item: <Education>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(
    education.value.action,
    "education",
    education.value.itemId,
    form
  );
  education.value.action = "";
  education.value.itemId = "";
}
</script>

<template>
  <ActionHeader
    :id="'education'"
    :header="'Образование'"
    :action="education.action"
    @action="education.action = education.action ? '' : 'create'"
  />
  <EducationForm
    v-if="education.action === 'create'"
    @submit="submitForm"
    @cancel="
      education.action = '';
      education.itemId = '';
    "
  />
  <div
    v-if="stateAnketa.anketa.education.length"
    :class="{ 'collapse show': !stateAnketa.share.printPage }"
    id="education"
  >
    <div
      class="mb-3"
      v-for="(item, idx) in stateAnketa.anketa.education"
      :key="idx"
      @mouseover="education.showActions = true"
      @mouseout="education.showActions = false"
      :class="{ 'card card-body': !stateAnketa.share.printPage }"
    >
      <EducationForm
        v-if="
          education.action === 'update' &&
          education.itemId === item['id'].toString()
        "
        :education="education.item"
        @submit="submitForm"
        @cancel="
          education.action = '';
          education.itemId = '';
        "
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="education.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'education')"
            @update="
              education.action = 'update';
              education.item = item;
              education.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'Вид образования'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Название учебного заведения'">{{
          item["name"]
        }}</LabelSlot>
        <LabelSlot :label="'Год окончания'">{{ item["finish"] }}</LabelSlot>
        <LabelSlot :label="'Специальность'">{{ item["speciality"] }}</LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
