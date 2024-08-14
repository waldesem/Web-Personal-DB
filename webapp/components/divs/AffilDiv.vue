<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Affilation } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const affilation = ref({} as Affilation);

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <div v-if="collapse" class="p-1">
    <div class="border rounded p-3">
      <FormsAffilationForm @cancel="cancelAction" />
    </div>
  </div>
  <div v-if="anketaState.anketa.value.affilations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.affilations"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
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
          <ElementsNaviHorizontal
            v-show="
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']
            "
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'affilations')"
            @update="
              affilation = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>
