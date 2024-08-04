<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "../../utils/state";
import type { Affilation } from "../../utils/interfaces";

const actions = ref(false);
const edit = ref(false);
const itemId = ref('');
const affilation = ref(<Affilation>{});

function cancelAction(){
  edit.value = false;
  itemId.value = "";
  const collapseContact = document.getElementById('affilationer');
  collapseContact?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <ElementsDropDownHead :id="'affilationer'" :header="'Аффилированность'"/>  
  <div class="collapse card card-body mb-3" id="affilationer">
    <FormsAffilationForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.affilations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.affilations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
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
                stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
                stateAnketa.anketa.persons['standing']
              "
            @delete="
              stateAnketa.deleteItem(item['id'].toString(), 'affilations')
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