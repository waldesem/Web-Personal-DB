<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa, stateUser } from "@/state";
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

const actions = ref(false);
const edit = ref(false);
const itemId = ref('');
const workplace = ref(<Work>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapseWork = document.getElementById("worker");
  collapseWork?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <DropDownHead :id="'worker'" :header="'Работа'" />
  <div class="collapse card card-body mb-3" id="worker">
    <WorkplaceForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.workplaces.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.workplaces"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <WorkplaceForm 
        v-if="edit && itemId == item['id'].toString()" 
        :work="workplace" 
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
              stateAnketa.deleteItem(item['id'].toString(), 'workplaces')
            "
            @update="
              workplace = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot v-if="item['now_work']" :label="'Текущая работа'">
          {{ item["now_work"] ? "Да" : "Нет" }}
        </LabelSlot>
        <LabelSlot :label="'Начало работы'">
          {{ new Date(item["starts"]).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot v-if="!item['now_work']" :label="'Окончание работы'">
          {{ new Date(item["finished"]).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot :label="'Место работы'">
          {{ item["workplace"] }}
        </LabelSlot>
        <LabelSlot :label="'Адрес'">
          {{ item["addresses"] }}
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
