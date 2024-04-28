<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { stateClassify, stateAnketa } from "@/state";
import type { Resume } from "@/interfaces";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
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
});
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
    class="px-3"
    @mouseover="dataResume.showActions = true"
    @mouseout="dataResume.showActions = false"
  >
    <LabelSlot>
      <ActionIcons
        v-show="dataResume.showActions"
        @delete="
          stateAnketa.deleteItem(stateAnketa.anketa.resume['id'], 'resume')
        "
        @update="dataResume.action = 'update'"
        :disable="
          stateClassify.status[stateAnketa.anketa.resume['status_id']] ===
          'finish'
        "
      >
      <FileForm 
        v-show="dataResume.showActions" 
        :accept="'*'" 
        @submit="stateAnketa.submitFile($event, 'resume')" 
      />
    </ActionIcons>
    </LabelSlot>
    <LabelSlot :label="'ID'">
      {{ stateAnketa.anketa.resume["id"] }}
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
      {{ stateAnketa.anketa.resume["country"] }}
    </LabelSlot>
    <LabelSlot :label="'Двойное гражданство'">
      {{ stateAnketa.anketa.resume["ext_country"] }}
    </LabelSlot>
    <LabelSlot :label="'СНИЛС'">
      {{ stateAnketa.anketa.resume["snils"] }}
    </LabelSlot>
    <LabelSlot :label="'ИНН'">
      {{ stateAnketa.anketa.resume["inn"] }}
    </LabelSlot>
    <LabelSlot :label="'Семейнное положение'">
      {{ stateAnketa.anketa.resume["marital"] }}
    </LabelSlot>
    <LabelSlot :label="'Дополнительная информация'">
      {{ stateAnketa.anketa.resume["addition"] }}
    </LabelSlot>
    <LabelSlot :label="'Статус'">
      {{ stateClassify.status[stateAnketa.anketa.resume["status_id"]] }}
    </LabelSlot>
    <LabelSlot :label="'Дата создания'">
      {{
        stateAnketa.anketa.resume["created"]
          ? new Date(
              String(stateAnketa.anketa.resume["created"])
            ).toLocaleDateString("ru-RU")
          : ""
      }}
    </LabelSlot>
    <LabelSlot :label="'Дата обновления'">
      {{
        stateAnketa.anketa.resume["updated"]
          ? new Date(
              String(stateAnketa.anketa.resume["updated"])
            ).toLocaleDateString("ru-RU")
          : ""
      }}
    </LabelSlot>
    <LabelSlot :label="'Пользователь'">
      {{
        stateAnketa.anketa.resume["user_id"]
          ? stateClassify.users[stateAnketa.anketa.resume["user_id"]]
          : ""
      }}
    </LabelSlot>
    <LabelSlot :label="'Материалы'">
      {{ stateAnketa.anketa.resume["path"] }}
    </LabelSlot>
  </div>
  <hr/>
  <div
    class="mb-3 px-3"
    v-for="(component, idx) in [
      PreviousDiv,
      EducationDiv,
      StaffDiv,
      DocumentDiv,
      AddressDiv,
      ContactDiv,
      RelationDiv,
      WorkplaceDiv,
      AffilationDiv,
    ]"
    :key="idx"
  >
    <component :is="component"/>
  </div>
</template>
