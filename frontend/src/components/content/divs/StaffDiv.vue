<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Staff } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const StaffForm = defineAsyncComponent(
  () => import("@components/content/forms/StaffForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(() => {
  stateAnketa.getItem("staff");
});

const staff = ref({
  action: "",
  itemId: "",
  item: <Staff>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(staff.value.action, "staff", staff.value.itemId, form);
  staff.value.action = "";
}
</script>

<template>
  <ActionHeader
    :id="'staff'"
    :header="'Должности'"
    :action="staff.action"
    @action="staff.action = staff.action ? '' : 'create'"
  />
  <StaffForm 
    v-if="staff.action" 
    :staff="staff.item" 
    @submit="submitForm" 
    @cancel="staff.action = ''"
  />
  <div v-else
    @mouseover="staff.showActions = true"
    @mouseout="staff.showActions = false"
  >
    <div 
      v-if="stateAnketa.anketa.staff.length" 
      :class="{'collapse show': !stateAnketa.share.printPage}" 
      id="staff"> 
      <div class="mb-3" v-for="(item, idx) in stateAnketa.anketa.staff" :key="idx">
        <div class="card card-body">
          <LabelSlot>
            <ActionIcons v-show="staff.showActions"
              @delete="stateAnketa.deleteItem(item['id'].toString(), 'staff')"
              @update="
                staff.action = 'update';
                staff.item = item;
                staff.itemId = item['id'].toString();
              "
            />
          </LabelSlot>
          <LabelSlot :label="'Должность'">{{ item["position"] }}</LabelSlot>
          <LabelSlot :label="'Департамент'">{{ item["department"] }}</LabelSlot>
        </div>
      </div>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
