<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateClassify, stateUser } from "@/state/state";
import type { Persons } from "@/utils/interfaces";

const StaffDiv = resolveComponent('DivsStaffDiv');
const EducateDiv = resolveComponent('DivsEducateDiv');
const WorkDiv = resolveComponent('DivsWorkDiv');
const DocumDiv = resolveComponent('DivsDocumDiv');
const AddressDiv = resolveComponent('DivsAddressDiv');
const ContactDiv = resolveComponent('DivsContactDiv');
const AffilDiv = resolveComponent('DivsAffilDiv');
const PrevDiv = resolveComponent('DivsPrevDiv');
const RelateDiv = resolveComponent('DivsRelateDiv');

const anketaState = stateAnketa();
const classifyState = stateClassify();
const userState = stateUser();

const dataResume = ref({
  action: "",
  form: <Persons>{},
  showActions: false,
});
</script>

<template>
  <div v-if="dataResume.action" class="card card-body mb-3">
    <FormsResumeForm
      :action="dataResume.action"
      :resume="anketaState.anketa.value.persons"
      @cancel="
        dataResume.action = '';
        anketaState.getItem('persons');
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
          anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
          anketaState.anketa.value.persons['standing']
        "
        @delete="
          anketaState.deleteItem(anketaState.anketa.value.persons['id'], 'persons')
        "
        @update="dataResume.action = 'update'"
      >
        <FormsFileForm
          :accept="'*'"
          @submit="
            anketaState.submitFile($event, 'anketa', anketaState.share.value.candId)
          "
        />
      </ElementsActionIcons>
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Регион'">
      <ElementsSelectDiv
        :width="'20%'"
        :name="'region'"
        :disable="
          userState.user.value.userId != anketaState.anketa.value.persons['user_id'] ||
          !anketaState.anketa.value.persons['standing']
        "
        :select="classifyState.classes.value.regions"
        v-model="anketaState.anketa.value.persons['region']"
        @submit-data="anketaState.changeRegion()"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Фамилия'">
      {{ anketaState.anketa.value.persons["surname"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Имя'">
      {{ anketaState.anketa.value.persons["firstname"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Отчество'">
      {{ anketaState.anketa.value.persons["patronymic"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата рождения'">
      {{
        new Date(
          String(anketaState.anketa.value.persons["birthday"])
        ).toLocaleDateString("ru-RU")
      }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Место рождения'">
      {{ anketaState.anketa.value.persons["birthplace"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Гражданство'">
      {{ anketaState.anketa.value.persons["citizenship"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="anketaState.anketa.value.persons['dual']"
      :label="'Двойное гражданство'"
    >
      {{ anketaState.anketa.value.persons["dual"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'СНИЛС'">
      {{ anketaState.anketa.value.persons["snils"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'ИНН'">
      {{ anketaState.anketa.value.persons["inn"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Семейное положение'">
      {{ anketaState.anketa.value.persons["marital"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата записи'">
      {{
        anketaState.anketa.value.persons["created"]
          ? new Date(
            anketaState.anketa.value.persons["created"] + " UTC"
            ).toLocaleString("ru-RU")
          : ""
      }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Пользователь'">
      {{
        anketaState.anketa.value.persons["username"]
          ? anketaState.anketa.value.persons["username"]
          : ""
      }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Материалы'">
      {{ anketaState.anketa.value.persons["destination"] }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дополнительная информация'">
      {{
        anketaState.anketa.value.persons["addition"]
          ? anketaState.anketa.value.persons["addition"]
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
