<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Inquisition } from "@/utils/interfaces";

const anketaState = stateAnketa();

await anketaState.getItem('investigations);

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const inquisition = ref({} as Inquisition);

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}

const editState = inject("editState") as boolean
</script>

<template>
  <UButton
    v-if="editState"
    class="py-3"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsInvestigationForm @cancel="cancelAction" />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.investigations.length">
    <UCard v-for="(item, index) in anketaState.anketa.value.investigations" :key="index">
      <template #header>
        <div class="tex-base text-red-800 font-medium" >
          {{ "Расследование/проверка ID #" + item["id"] }}
        </div>
      </template>
      <FormsInvestigationForm
        v-if="
          edit &&
          itemId ==
            anketaState.anketa.value.investigations[index]['id'].toString()
        "
        :investigation="inquisition"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot :label="'Тема проверки'">{{
          anketaState.anketa.value.investigations[index]["theme"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Информация'">{{
          anketaState.anketa.value.investigations[index]["info"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{
          anketaState.anketa.value.investigations[index]["username"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{
            new Date(
              anketaState.anketa.value.investigations[index]["created"] +
                " UTC"
            ).toLocaleString("ru-RU")
          }}
        </ElementsLabelSlot>
      </div>
      <template
        v-if="
          editState &&
          (!edit && itemId !=
          anketaState.anketa.value.investigations[index]['id'].toString())
        "
      >
        <ElementsNaviHorizont
          v-show="!index && editState"
          @update="
            inquisition = anketaState.anketa.value.investigations[index];
            itemId =
              anketaState.anketa.value.investigations[index][
                'id'
              ].toString();
            edit = true;
          "
          @delete="
            anketaState.deleteItem(
              anketaState.anketa.value.investigations[index][
                'id'
              ].toString(),
              'investigations'
            )
          "
          @upload="openFileForm('investigation-file')"
        />
        <div v-show="false">
          <UInput
            id="investigation-file"
            type="file"
            accept="*"
            multiple
            @change="
              anketaState.submitFile(
                $event,
                'investigations',
                anketaState.share.value.candId
              )
            "
          />
        </div>
      </template>
    </UCard>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Расследования/Проверки не проводились</p>
  </div>
</template>

