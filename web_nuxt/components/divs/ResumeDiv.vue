<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Persons } from "@/utils/interfaces";

const anketaState = stateAnketa();
const classifyState = stateClassify();

const dataResume = ref({
  action: "",
  form: {} as Persons,

  openFileForm(elementId: string) {
    document.getElementById(elementId)?.click();
  },
});

const editState = inject("editState") as boolean
</script>

<template>
  <UCard>
    <div v-if="dataResume.action">
      <FormsResumeForm
        :action="dataResume.action"
        :resume="anketaState.anketa.value.persons"
        @cancel="
          dataResume.action = '';
          anketaState.getItem('persons');
        "
      />
     </div>
    <div v-else>
      <ElementsLabelSlot :label="'Регион'">
        <USelect
          v-model="anketaState.anketa.value.persons['region']"
          style="width: 20%;"
          :options="Object.values(classifyState.classes.value.regions)"
          :disabled="!editState"
          @change="anketaState.changeRegion()"
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
        <a 
          class="text-red-500"
          target="_blank" 
          :href="anketaState.anketa.value.persons['destination']">
          Открыть
        </a>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дополнительная информация'">
        {{
          anketaState.anketa.value.persons["addition"]
            ? anketaState.anketa.value.persons["addition"]
            : "-"
        }}
      </ElementsLabelSlot>
    </div>
    <template
      v-if="editState && !dataResume.action"
      #footer
    >
      <ElementsNaviHorizont
        v-show="editState"
        @delete="
          anketaState.deleteItem(
            anketaState.anketa.value.persons['id'],
            'persons'
          )
        "
        @update="dataResume.action = 'update'"
        @upload="dataResume.openFileForm('resume-file')"
      />
      <div v-show="false">
        <UInput
          id="resume-file"
          type="file"
          accept="*"
          multiple
          @change="
            anketaState.submitFile(
              $event,
              'anketa',
              anketaState.share.value.candId
            )
          "
        />
      </div>
    </template>
  </UCard>
</template>