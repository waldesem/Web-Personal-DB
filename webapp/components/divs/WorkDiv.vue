<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Work } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

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
  <ElementsDropDownHead :id="'worker'" :header="'Работа'" />
  <div class="collapse card card-body mb-3" id="worker">
    <FormsWorkplaceForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.workplaces.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.workplaces"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <FormsWorkplaceForm 
        v-if="edit && itemId == item['id'].toString()" 
        :work="workplace" 
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
              anketaState.deleteItem(item['id'].toString(), 'workplaces')
            "
            @update="
              workplace = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot v-if="item['now_work']" :label="'Текущая работа'">
          {{ item["now_work"] ? "Да" : "Нет" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Начало работы'">
          {{ new Date(item["starts"]).toLocaleDateString("ru-RU") }}
        </ElementsLabelSlot>
        <ElementsLabelSlot v-if="!item['now_work']" :label="'Окончание работы'">
          {{ new Date(item["finished"]).toLocaleDateString("ru-RU") }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Место работы'">
          {{ item["workplace"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Адрес'">
          {{ item["addresses"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Должность'">
          {{ item["position"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot v-if="item['reason']" :label="'Причина увольнения'">
          {{ item["reason"] }}
        </ElementsLabelSlot>
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
