<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Staff } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const edit = ref(false);
const itemId = ref('');
const staff = ref(<Staff>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapseStaff = document.getElementById("staffer");
  collapseStaff?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <ElementsDropDownHead :id="'staffer'" :header="'Должности'" />
  <div class="collapse card card-body mb-3" id="staffer">
    <FormsStaffForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.staffs.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.staffs"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <FormsStaffForm 
        v-if="edit && itemId == item['id'].toString()"  
        :staff="staff"
        @cancel="cancelAction" 
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="actions &&
                anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
                anketaState.anketa.value.persons['standing']"
            @delete="anketaState.deleteItem(item['id'].toString(), 'staffs')"
            @update="
              staff = item;
              edit = true;
              itemId = item['id'].toString()
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Должность'">{{ item["position"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Департамент'">{{ item["department"] }}</ElementsLabelSlot>
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
