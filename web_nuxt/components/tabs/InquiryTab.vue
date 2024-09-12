<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Needs } from "@/utils/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const need = ref({} as Needs);

const { refresh } = await useLazyAsyncData("inquiries", async () => {
  await anketaState.getItem('inquiries')
})

async function updateNeed(needForm: Needs) {
  Promise.all([
    await anketaState.updateItem("inquiries", needForm),
    await refresh()
  ])
  closeAction();
}

async function deleteNeed(index: string) {
  closeAction();
  Promise.all([
    await anketaState.deleteItem(index, 'inquiries'),
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
        <FormsInquiryForm 
          @cancel="cancelOperation" 
          @submit="updateNeed"
        />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.inquiries.length">
    <div 
      v-for="(item, index) in anketaState.anketa.value.inquiries" :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
      >
      <UCard>
        <template #header>
          <div class="tex-base text-red-800 font-medium" >
            {{ "Запрос о сотруднике ID #" + item["id"] }}
          </div>
        </template>
        <FormsInquiryForm
          v-if="
            edit &&
            itemId ==
              anketaState.anketa.value.inquiries[index]['id'].toString()
          "
          :inquiry="need"
          @cancel="cancelOperation"
          @submit="updateNeed"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Информация'">{{
            anketaState.anketa.value.inquiries[index]["info"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Иннициатор'">{{
            anketaState.anketa.value.inquiries[index]["initiator"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Источники'">{{
            anketaState.anketa.value.inquiries[index]["origins"]
          }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            anketaState.anketa.value.inquiries[index]["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{
              new Date(
                anketaState.anketa.value.inquiries[index]["created"] + " UTC"
              ).toLocaleString("ru-RU")
            }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="
            editState &&
            !edit &&
            itemId !=
              anketaState.anketa.value.inquiries[index]['id'].toString()
          "
          #footer 
        >
          <ElementsNaviHorizont
            v-show="!index && editState"
            @delete="
              deleteNeed(
                anketaState.anketa.value.inquiries[index]['id']
              )
            "
            @update="
              need = anketaState.anketa.value.inquiries[index];
              itemId =
                anketaState.anketa.value.inquiries[index]['id'].toString();
              edit = true;
            "
            @upload="openFileForm('inquiry-file')"
          />
          <div v-show="false">
            <UInput
              id="inquiry-file"
              type="file"
              accept="*"
              multiple
              @change="
                anketaState.submitFile(
                  $event,
                  'inquiries',
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
    <p class="text-primary">Запросы о сотруднике не поступали</p>
  </div>
</template>

