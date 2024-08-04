<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa, stateClassify, stateUser } from "../../utils/state";
import type { Persons } from "../../utils/interfaces";

const StaffDiv = defineAsyncComponent(
  () => import("../../components/divs/StaffDiv.vue")
);
const EducateDiv = defineAsyncComponent(
  () => import("../../components/divs/EducateDiv.vue")
);
const WorkDiv = defineAsyncComponent(
  () => import("../../components/divs/WorkDiv.vue")
);
const DocumDiv = defineAsyncComponent(
  () => import("../../components/divs/DocumDiv.vue")
);
const AddressDiv = defineAsyncComponent(
  () => import("../../components/divs/AddressDiv.vue")
);
const ContactDiv = defineAsyncComponent(
  () => import("../../components/divs/ContactDiv.vue")
);
const AffilDiv = defineAsyncComponent(
  () => import("../../components/divs/AffilDiv.vue")
);
const PrevDiv = defineAsyncComponent(
  () => import("../../components/divs/PrevDiv.vue")
);
const RelateDiv = defineAsyncComponent(
  () => import("../../components/divs/RelateDiv.vue")
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
    <ElementsLabelSlot>
      <ElementsActionIcons
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
      </ElementsActionIcons>
    </ElementsLabelSlot>
    <ElementsLabelSlot class="d-print-none" :label="'Регион'">
      <ElementsSelectDiv
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
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Фамилия'">
      {{ stateAnketa.anketa.persons["surname"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Имя'">
      {{ stateAnketa.anketa.persons["firstname"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Отчество'">
      {{ stateAnketa.anketa.persons["patronymic"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата рождения'">
      {{
        new Date(
          String(stateAnketa.anketa.persons["birthday"])
        ).toLocaleDateString("ru-RU")
      }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Место рождения'">
      {{ stateAnketa.anketa.persons["birthplace"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Гражданство'">
      {{ stateAnketa.anketa.persons["citizenship"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="stateAnketa.anketa.persons['dual']"
      :label="'Двойное гражданство'"
    >
      {{ stateAnketa.anketa.persons["dual"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'СНИЛС'">
      {{ stateAnketa.anketa.persons["snils"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'ИНН'">
      {{ stateAnketa.anketa.persons["inn"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Семейное положение'">
      {{ stateAnketa.anketa.persons["marital"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата записи'">
      {{
        stateAnketa.anketa.persons["created"]
          ? new Date(
              stateAnketa.anketa.persons["created"] + " UTC"
            ).toLocaleString("ru-RU")
          : ""
      }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Пользователь'">
      {{
        stateAnketa.anketa.persons["username"]
          ? stateAnketa.anketa.persons["username"]
          : ""
      }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Материалы'">
      {{ stateAnketa.anketa.persons["destination"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дополнительная информация'">
      {{
        stateAnketa.anketa.persons["addition"]
          ? stateAnketa.anketa.persons["addition"]
          : "-"
      }}
    </ElementsLabelSlot>
  </div>
  <div
    v-for="(component, idx) in [
      StaffDiv,
      EducateDiv,
      WorkDiv,
      DocumDiv,
      AddressDiv,
      ContactDiv,
      AffilDiv,
      PrevDiv,
      RelateDiv,
    ]"
    :key="idx"
  >
    <component :is="component" />
  </div>
</template>
