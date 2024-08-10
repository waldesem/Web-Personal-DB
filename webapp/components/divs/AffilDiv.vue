<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Affilation } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const collapse = ref(false);
const edit = ref(false);
const itemId = ref('');
const affilation = ref(<Affilation>{});

function cancelAction(){
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
};
</script>

<template>
  <UButton label="Аффилирован" variant="link" @click="collapse = !collapse" />  
  <div class="border rounded m-3">
    <FormsAffilationForm @cancel="cancelAction"/>
  </div>
  <div v-if="anketaState.anketa.value.affilations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.affilations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="border rounded m-3"
    >
      <FormsAffilationForm
        v-if="edit && itemId == item['id'].toString()" 
        :affils="affilation"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
                actions &&
                anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
                anketaState.anketa.value.persons['standing']
              "
            @delete="
              anketaState.deleteItem(item['id'].toString(), 'affilations')
            "
            @update="
              affilation = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Тип участия'">{{ item["view"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Организация'">{{ item["organization"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'ИНН'">{{ item["inn"] }}</ElementsLabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>