<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Pfo } from "@/utils/interfaces";

const anketaState = stateAnketa();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const poligraf = ref({} as Pfo);

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
        <FormsPoligrafForm @cancel="cancelAction" />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.poligrafs.length">
    <UCard v-for="(item, index) in anketaState.anketa.value.poligrafs" :key="index">
      <template #header>
        <div class="tex-base text-red-800 font-medium" >
          {{ "Обследование на полиграфе ID #" + item["id"] }}
        </div>
      </template>
      <FormsPoligrafForm
        v-if="
          edit &&
          itemId ==
            anketaState.anketa.value.poligrafs[index]['id'].toString()
        "
        :poligraf="poligraf"
        @cancel="cancelAction"
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
        <ElementsNaviHorizont
          v-show="!index && editState"
          @update="
            poligraf = anketaState.anketa.value.poligrafs[index];
            itemId =
              anketaState.anketa.value.poligrafs[index]['id'].toString();
            edit = true;
          "
          @delete="
            anketaState.deleteItem(
              anketaState.anketa.value.poligrafs[index]['id'].toString(),
              'poligrafs'
            )
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
      </div>
    </UCard>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Обследование на полиграфе не проводилось</p>
  </div>
</template>

