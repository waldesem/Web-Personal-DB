<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
import { Work } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/content/forms/WorkplaceForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const workplace = ref({
  itemId: "",
  item: <Work>{},
  showActions: false,
});

function cancelAction(){
  workplace.value.itemId = "";
  Object.keys(workplace.value.item).forEach(
    (key) => delete workplace.value.item[key as keyof typeof workplace.value.item]
  );
  const collapseWork = document.getElementById('work');
  collapseWork?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <DropDownHead :id="'work'" :header="'Работа'"/>
  <div class="collapse card card-body mb-3" id="work">
    <WorkplaceForm @cancel="cancelAction" />
  </div>
  <div
    v-if="stateAnketa.anketa.workplaces.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.workplaces"
      :key="idx"
      @mouseover="workplace.showActions = true"
      @mouseout="workplace.showActions = false"
      class="card card-body mb-3"
    >
      <WorkplaceForm
        v-if="workplace.itemId === item['id'].toString()"
        :work="workplace.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="workplace.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'workplaces')"
            @update="
              workplace.item = item;
              workplace.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot v-if="item['now_work']" :label="'Текущая работа'">
          {{ item["now_work"] ? "Да" : "Нет" }}
        </LabelSlot>
        <LabelSlot :label="'Начало работы'">
          {{ new Date(item["started"]).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot v-if="!item['now_work']" :label="'Окончание работы'">
          {{ new Date(item["finished"]).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot :label="'Место работы'">
          {{ item["workplace"] }}
        </LabelSlot>
        <LabelSlot :label="'Адрес'">
          {{ item["address"] }}
        </LabelSlot>
        <LabelSlot :label="'Должность'">
          {{ item["position"] }}
        </LabelSlot>
        <LabelSlot v-if="item['reason']" :label="'Причина увольнения'">
          {{ item["reason"] }}
        </LabelSlot>
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