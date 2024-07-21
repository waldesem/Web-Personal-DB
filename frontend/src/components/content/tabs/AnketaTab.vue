<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { stateAnketa, stateClassify, stateUser } from "@/state";
import type { Persons } from "@/interfaces";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
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
  form: <Persons>{},
  showActions: false,
});
</script>

<template>
  <div v-if="dataResume.action" class="card card-body mb-3">
    <ResumeForm
      :action="dataResume.action"
      :resume="stateAnketa.anketa.persons"
      @cancel="
        dataResume.action = '';
        stateAnketa.getItem('persons');
      "
    />
  </div>
  <div
    v-else
    class="card card-body mb-3"
    @mouseover="dataResume.showActions = true"
    @mouseout="dataResume.showActions = false"
  >
    <LabelSlot>
      <ActionIcons
        v-show="
          dataResume.showActions &&
          stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
          stateAnketa.anketa.persons['standing']
        "
        @delete="
          stateAnketa.deleteItem(stateAnketa.anketa.persons['id'], 'persons')
        "
        @update="dataResume.action = 'update'"
        :for-input="'persons-file'"
      >
        <FileForm
          v-show="dataResume.showActions"
          :name-id="'persons-file'"
          :accept="'*'"
          @submit="
            stateAnketa.submitFile($event, 'anketa', stateAnketa.share.candId)
          "
        />
      </ActionIcons>
    </LabelSlot>
    <LabelSlot :label="'Регион'">
      <SelectDiv
        :width="'20%'"
        :name="'region'"
        :disable="
          stateUser.user.userId != stateAnketa.anketa.persons['user_id'] ||
          !stateAnketa.anketa.persons['standing']
        "
        :select="stateClassify.classes.regions"
        v-model="stateAnketa.anketa.persons['region']"
        @submit-data="stateAnketa.changeRegion()"
      />
    </LabelSlot>
    <LabelSlot :label="'Фамилия'">
      {{ stateAnketa.anketa.persons["surname"] }}
    </LabelSlot>
    <LabelSlot :label="'Имя'">
      {{ stateAnketa.anketa.persons["firstname"] }}
    </LabelSlot>
    <LabelSlot :label="'Отчество'">
      {{ stateAnketa.anketa.persons["patronymic"] }}
    </LabelSlot>
    <LabelSlot :label="'Дата рождения'">
      {{
        new Date(
          String(stateAnketa.anketa.persons["birthday"])
        ).toLocaleDateString("ru-RU")
      }}
    </LabelSlot>
    <LabelSlot :label="'Место рождения'">
      {{ stateAnketa.anketa.persons["birthplace"] }}
    </LabelSlot>
    <LabelSlot :label="'Гражданство'">
      {{ stateAnketa.anketa.persons["citizenship"] }}
    </LabelSlot>
    <LabelSlot
      v-if="stateAnketa.anketa.persons['dual']"
      :label="'Двойное гражданство'"
    >
      {{ stateAnketa.anketa.persons["dual"] }}
    </LabelSlot>
    <LabelSlot :label="'СНИЛС'">
      {{ stateAnketa.anketa.persons["snils"] }}
    </LabelSlot>
    <LabelSlot :label="'ИНН'">
      {{ stateAnketa.anketa.persons["inn"] }}
    </LabelSlot>
    <LabelSlot :label="'Семейное положение'">
      {{ stateAnketa.anketa.persons["marital"] }}
    </LabelSlot>
    <LabelSlot :label="'Дата записи'">
      {{
        stateAnketa.anketa.persons["created"]
          ? new Date(
              stateAnketa.anketa.persons["created"] + " UTC"
            ).toLocaleString("ru-RU")
          : ""
      }}
    </LabelSlot>
    <LabelSlot :label="'Пользователь'">
      {{
        stateAnketa.anketa.persons["username"]
          ? stateAnketa.anketa.persons["username"]
          : ""
      }}
    </LabelSlot>
    <LabelSlot :label="'Материалы'">
      {{ stateAnketa.anketa.persons["destination"] }}
    </LabelSlot>
    <LabelSlot :label="'Дополнительная информация'">
      {{
        stateAnketa.anketa.persons["addition"]
          ? stateAnketa.anketa.persons["addition"]
          : "-"
      }}
    </LabelSlot>
  </div>
  <div
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
    <component :is="component" />
  </div>
</template>
