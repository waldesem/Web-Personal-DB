<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Inquisition } from "@/utils/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const inquisition = ref({} as Inquisition);

const { refresh } = await useAsyncData("investigations", async () => {
  await anketaState.getItem('investigations');
})

async function updateInquisition(inquisitionForm: Inquisition) {
  Promise.all([
    await anketaState.updateItem("investigations", inquisitionForm),
    await refresh()
  ])
  closeAction();
}

async function deleteInquisition(index: string) {
  Promise.all([
    await anketaState.deleteItem(index, 'investigations'),
    await refresh()
  ])
}

async function cancelOperation() {
  await refresh();
  closeAction();
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}
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
        <FormsInvestigationForm 
        @cancel="cancelOperation" 
        @submit="updateInquisition"
      />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.investigations.length">
    <div 
      v-for="(item, index) in anketaState.anketa.value.investigations" :key="index"
      class="py-1"
      >
      <UCard>
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
          @cancel="cancelOperation"
          @submit="updateInquisition"
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
              deleteInquisition(
                anketaState.anketa.value.investigations[index][
                  'id'],
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
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Расследования/Проверки не проводились</p>
  </div>
</template>

