<script setup lang="ts">
import { useFetchAuth } from "@/utils/auth";
import { server, stateAnketa, stateClassify } from "@/state/state";
import type { Persons } from "@/utils/interfaces";

const authFetch = useFetchAuth();

const toast = useToast();

const anketaState = stateAnketa();

const classifyState = stateClassify();

const editState = inject("editState") as boolean

const dataResume = ref({
  action: "",
  skeleton: false,
  form: {} as Persons,
});

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}

async function changeRegion(): Promise<void> {
  if (!confirm("Вы действительно хотите изменить регион?")) return;
  const response = await authFetch(`${server}/region/${anketaState.share.value.candId}`, {
    params: {
      region: anketaState.anketa.value.persons["region"],
    },
  });
  console.log(response);
  anketaState.getItem("persons");
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: "Изменение региона успешно",
    color: "green",
  });
}

function deleteItem() {
  anketaState.deleteItem(anketaState.anketa.value.persons['id'], 'persons');
  navigateTo('/persons');
}

function updateItem(form: Persons) {
  dataResume.action = "";
  anketaState.updateItem("persons", form)
}

function cancelAction(){
  dataResume.action = '';
  anketaState.getItem('persons');
}
</script>

<template>
  <UCard>
    <div v-if="dataResume.action">
      <FormsResumeForm
        :action="dataResume.action"
        :resume="anketaState.anketa.value.persons"
        @cancel="cancelAction"
        @update="updateItem"
      />
     </div>
    <div v-else>
      <ElementsLabelSlot :label="'Регион'">
        <USelect
          v-model="anketaState.anketa.value.persons['region']"
          style="width: 20%;"
          :options="Object.values(classifyState.classes.value.regions)"
          :disabled="!editState"
          @change="changeRegion()"
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
      <ElementsLabelSlot :label="'Материалы'"> {{ anketaState.anketa.value.persons['destination'] }}
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
        @delete="deleteItem"
        @update="dataResume.action = 'update'"
        @upload="openFileForm('resume-file')"
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