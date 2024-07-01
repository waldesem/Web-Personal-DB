<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
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

const affilation = ref({
  itemId: "",
  item: <Affilation>{},
  showActions: false,
});

function cancelAction(){
  affilation.value.itemId = "";
  Object.keys(affilation.value.item).forEach(
    (key) => delete affilation.value.item[key as keyof typeof affilation.value.item]
  );
  const collapseContact = document.getElementById('affilation');
  collapseContact?.setAttribute('class', 'collapse card card-body');
};
</script>

<template>
  <DropDownHead :id="'affilation'" :header="'Аффилированность'"/>  <div class="collapse card card-body" id="affilation">
    <AffilationForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.affilations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.affilations"
      :key="idx"
      @mouseover="affilation.showActions = true"
      @mouseout="affilation.showActions = false"
      class="card card-body"
    >
      <AffilationForm
        v-if="affilation.itemId === item['id'].toString()"
        :affils="affilation.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="affilation.showActions"
            @delete="
              stateAnketa.deleteItem(item['id'].toString(), 'affilations')
            "
            @update="
              affilation.item = item;
              affilation.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Тип участия'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Организация'">{{ item["name"] }}</LabelSlot>
        <LabelSlot :label="'ИНН'">{{ item["inn"] }}</LabelSlot>
        <LabelSlot :label="'Должность'">{{ item["position"] }}</LabelSlot>
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