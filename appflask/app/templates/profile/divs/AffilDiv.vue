<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa, stateUser } from "@/state";
import { Affilation } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/content/forms/AffilationForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

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
  <DropDownHead :id="'affilationer'" :header="'Аффилированность'"/>  
  <div class="collapse card card-body mb-3" id="affilationer">
    <AffilationForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.affilations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.affilations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <AffilationForm
        v-if="edit && itemId == item['id'].toString()" 
        :affils="affilation"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
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
        </LabelSlot>
        <LabelSlot :label="'Тип участия'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Организация'">{{ item["organization"] }}</LabelSlot>
        <LabelSlot :label="'ИНН'">{{ item["inn"] }}</LabelSlot>
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