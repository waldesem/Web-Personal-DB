<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Pfo } from "@/types/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean;

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const poligraf = ref({} as Pfo);

const { refresh } = await useLazyAsyncData("poligrafs", async () => {
  await anketaState.getItem("poligrafs");
});

async function updatePoligraf(poligrafForm: Pfo) {
  closeAction();
  anketaState.updateItem("poligrafs", poligrafForm);
  refresh();
}

async function deletePoligraf(index: string) {
  closeAction();
  anketaState.deleteItem(index, "poligrafs");
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
        <FormsPoligrafForm @cancel="cancelOperation" @submit="updatePoligraf" />
      </UCard>
    </div>
  </Transition>
  <div
    v-if="
      anketaState.anketa.value.poligrafs &&
      anketaState.anketa.value.poligrafs.length
    "
  >
    <div
      v-for="(item, index) in anketaState.anketa.value.poligrafs"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <UCard>
        <template #header>
          <div class="tex-base text-red-800 font-medium">
            {{ "Обследование на полиграфе ID #" + item["id"] }}
          </div>
        </template>
        <FormsPoligrafForm
          v-if="
            edit &&
            itemId == anketaState.anketa.value.poligrafs[index]['id'].toString()
          "
          :poligraf="poligraf"
          @cancel="cancelOperation"
          @submit="updatePoligraf"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тема проверки'">{{
            anketaState.anketa.value.poligrafs[index]["theme"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Результат'">{{
            anketaState.anketa.value.poligrafs[index]["results"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            anketaState.anketa.value.poligrafs[index]["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{
              new Date(
                anketaState.anketa.value.poligrafs[index]["created"] + " UTC"
              ).toLocaleString("ru-RU")
            }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            @update="
              poligraf = anketaState.anketa.value.poligrafs[index];
              itemId =
                anketaState.anketa.value.poligrafs[index]['id'].toString();
              edit = true;
            "
            @delete="
              deletePoligraf(anketaState.anketa.value.poligrafs[index]['id'])
            "
            @upload="openFileForm('poligraf-file')"
          />
          <div v-show="false">
            <UInput
              id="poligraf-file"
              type="file"
              accept="*"
              multiple
              @change="
                anketaState.submitFile(
                  $event,
                  'poligrafs',
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
    <p class="text-red-800">Обследование на полиграфе не проводилось</p>
  </div>
</template>
