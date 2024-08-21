<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa, stateUser } from "@/state";
import { Staff } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const StaffForm = defineAsyncComponent(
  () => import("@components/content/forms/StaffForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

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
  <DropDownHead :id="'staffer'" :header="'Должности'" />
  <div class="collapse card card-body mb-3" id="staffer">
    <StaffForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.staffs.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.staffs"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <StaffForm 
        v-if="edit && itemId == item['id'].toString()"  
        :staff="staff"
        @cancel="cancelAction" 
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="actions &&
                stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
                stateAnketa.anketa.persons['editable']"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'staffs')"
            @update="
              staff = item;
              edit = true;
              itemId = item['id'].toString()
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Должность'">{{ item["position"] }}</LabelSlot>
        <LabelSlot :label="'Департамент'">{{ item["department"] }}</LabelSlot>
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
