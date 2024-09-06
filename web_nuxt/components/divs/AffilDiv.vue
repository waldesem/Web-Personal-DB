<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Affilation } from "@/utils/interfaces";

const anketaState = stateAnketa();

await anketaState.getItem('affilations');

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const affilation = ref({} as Affilation);

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
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsAffilationForm @cancel="cancelAction" />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.affilations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.affilations"
      :key="idx"
      class="p-1"
    >
      <UCard>
        <FormsAffilationForm
          v-if="edit && itemId == item['id'].toString()"
          :affils="affilation"
          @cancel="cancelAction"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тип участия'">{{
            item["view"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Организация'">{{
            item["organization"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'ИНН'">{{ item["inn"] }}</ElementsLabelSlot>
        </div>
        <template
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
        <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'affilations')"
            @update="
              affilation = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>

