<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { stateAnketa, submitFile } from "@/state";
import type { Resume } from "@/interfaces";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("@components/content/forms/ResumeForm.vue")
);
const PreviousDiv = defineAsyncComponent(
  () => import("@components/content/divs/PreviousDiv.vue")
);
const EducationDiv = defineAsyncComponent(
  () => import("@components/content/divs/EducationDiv.vue")
);
const StaffDiv = defineAsyncComponent(
  () => import("@components/content/divs/StaffDiv.vue")
);
const DocumentDiv = defineAsyncComponent(
  () => import("@components/content/divs/DocumentDiv.vue")
);
const AddressDiv = defineAsyncComponent(
  () => import("@components/content/divs/AddressDiv.vue")
);
const ContactDiv = defineAsyncComponent(
  () => import("@components/content/divs/ContactDiv.vue")
);
const RelationDiv = defineAsyncComponent(
  () => import("@components/content/divs/RelationDiv.vue")
);
const WorkplaceDiv = defineAsyncComponent(
  () => import("@components/content/divs/WorkplaceDiv.vue")
);
const AffilationDiv = defineAsyncComponent(
  () => import("@components/content/divs/AffilationDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const dataResume = ref({
  action: "",
  form: <Resume>{},
  showActions: false,
})
</script>

<template>
  <ResumeForm
    v-if="dataResume.action"
    :action="dataResume.action"
    :resume="stateAnketa.anketa.resume"
    @cancel="dataResume.action = ''"
  />
  <div
    v-else
    class="card card-body mb-3"
    @mouseover="dataResume.showActions = true"
    @mouseout="dataResume.showActions = false"
  >
    <LabelSlot>
      <ActionIcons
        v-show="dataResume.showActions"
        @delete="
          stateAnketa.deleteItem(stateAnketa.anketa.resume['id'], 'persons')
        "
        @update="dataResume.action = 'update'"
        :for-input="'persons-file'"
      >
      <FileForm
        v-show="dataResume.showActions" 
        :name-id="'persons-file'"
        :accept="'*'" 
        @submit="submitFile($event, 'persons')" 
      />
    </ActionIcons>
    </LabelSlot>
    <LabelSlot :label="'Фамилия'">
      {{ stateAnketa.anketa.resume["surname"] }}
    </LabelSlot>
    <LabelSlot :label="'Имя'">
      {{ stateAnketa.anketa.resume["firstname"] }}
    </LabelSlot>
    <LabelSlot :label="'Отчество'">
      {{ stateAnketa.anketa.resume["patronymic"] }}
    </LabelSlot>
    <LabelSlot :label="'Дата рождения'">
      {{
        new Date(
          String(stateAnketa.anketa.resume["birthday"])
        ).toLocaleDateString("ru-RU")
      }}
    </LabelSlot>
    <LabelSlot :label="'Место рождения'">
      {{ stateAnketa.anketa.resume["birthplace"] }}
    </LabelSlot>
    <LabelSlot :label="'Гражданство'">
      {{ stateAnketa.anketa.resume["citizenship"] }}
    </LabelSlot>
    <LabelSlot 
      v-if="stateAnketa.anketa.resume['dual']"
      :label="'Двойное гражданство'"
    >
      {{ stateAnketa.anketa.resume["dual"] }}
    </LabelSlot>
    <LabelSlot :label="'СНИЛС'">
      {{ stateAnketa.anketa.resume["snils"] }}
    </LabelSlot>
    <LabelSlot :label="'ИНН'">
      {{ stateAnketa.anketa.resume["inn"] }}
    </LabelSlot>
    <LabelSlot :label="'Семейное положение'">
      {{ stateAnketa.anketa.resume["marital"] }}
    </LabelSlot>
    <LabelSlot :label="'Статус'">
      {{ stateAnketa.anketa.resume["status"]   }}
    </LabelSlot>
    <LabelSlot :label="'Дата записи'">
      {{
        stateAnketa.anketa.resume["created"]
          ? new Date(
              stateAnketa.anketa.resume["created"]
            ).toLocaleString("ru-RU")
          : ""
      }}
    </LabelSlot>
    <LabelSlot :label="'Пользователь'">
      {{
        stateAnketa.anketa.resume["username"]
          ? stateAnketa.anketa.resume["username"]
          : ""
      }}
    </LabelSlot>
    <LabelSlot :label="'Материалы'">
      {{ stateAnketa.anketa.resume["path"] }}
    </LabelSlot>
    <LabelSlot :label="'Дополнительная информация'">
      {{ stateAnketa.anketa.resume["addition"] 
      ? stateAnketa.anketa.resume["addition"] : "-" }}
    </LabelSlot>
  </div>
  <div
    class="mb-3 px-3"
    v-for="(component, idx) in [
      StaffDiv,
      EducationDiv,
      WorkplaceDiv,
      DocumentDiv,
      AddressDiv,
      ContactDiv,
      AffilationDiv,
      PreviousDiv,
      RelationDiv,
    ]"
    :key="idx"
  >
    <component :is="component"/>
  </div>
  <hr/>
</template>
