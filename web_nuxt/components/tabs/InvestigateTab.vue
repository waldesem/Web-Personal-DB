<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Inquisition } from "@/types/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean;

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const inquisition = ref({} as Inquisition);

const { refresh } = await useLazyAsyncData("investigations", async () => {
  await anketaState.getItem("investigations");
});

async function updateInquisition(inquisitionForm: Inquisition) {
  closeAction();
  anketaState.updateItem("investigations", inquisitionForm);
  refresh();
}

async function deleteInquisition(index: string) {
  anketaState.deleteItem(index, "investigations");
  refresh();
}

async function cancelOperation() {
  closeAction();
  refresh();
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
  <div
    v-if="
      anketaState.anketa.value.investigations &&
      anketaState.anketa.value.investigations.length
    "
  >
    <div
      v-for="(item, index) in anketaState.anketa.value.investigations"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <UCard>
        <template #header>
          <div class="tex-base text-red-800 font-medium">
            {{ "Расследование/проверка ID #" + item["id"] }}
          </div>
        </template>
        <FormsInvestigationForm
          v-if="edit && itemId == item['id'].toString()"
          :investigation="inquisition"
          @cancel="cancelOperation"
          @submit="updateInquisition"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тема проверки'">{{
            item["theme"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Информация'">{{
            item["info"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            item["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            @update="
              inquisition = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @delete="deleteInquisition(item['id'])"
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
    <p class="text-red-800">Расследования/Проверки не проводились</p>
  </div>
</template>
