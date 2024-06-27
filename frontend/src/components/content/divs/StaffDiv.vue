<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
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

const staff = ref({
  itemId: "",
  item: <Staff>{},
  showActions: false,
});

function cancelAction(){
  staff.value.itemId = "";
  Object.keys(staff.value.item).forEach(
    (key) => delete staff.value.item[key as keyof typeof staff.value.item]
  );
  const collapseStaff = document.getElementById('staff');
  collapseStaff?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <DropDownHead :id="'staff'" :header="'Должности'"/>
  <div class="collapse card card-body mb-3" id="staff">
    <StaffForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.staffs.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.staffs"
      :key="idx"
      @mouseover="staff.showActions = true"
      @mouseout="staff.showActions = false"
      class="card card-body mb-3"
    >
      <StaffForm
        v-if="staff.itemId === item['id'].toString()"
        :staff="staff.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="staff.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'staffs')"
            @update="
              staff.item = item;
              staff.itemId = item['id'].toString();
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