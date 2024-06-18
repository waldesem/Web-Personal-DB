<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Staff } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
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

onBeforeMount(() => {
  stateAnketa.getItem("staffs");
});

const staff = ref({
  action: "",
  itemId: "",
  item: <Staff>{},
  showActions: false,
});

function cancelAction(){
  staff.value.action = "";
  staff.value.itemId = "";
  staff.value.item = <Staff>({});
};

function submitForm(form: Object) {
  stateAnketa.updateItem
  (
    "staffs", 
    form
  );
  cancelAction()
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
    v-if="staff.action === 'create'"
    @submit="submitForm"
    @cancel="cancelAction"
  />
  <div
    v-if="stateAnketa.anketa.staffs.length"
    class="collapse show"
    id="staff"
  >
    <div
      v-for="(item, idx) in stateAnketa.anketa.staffs"
      :key="idx"
      @mouseover="staff.showActions = true"
      @mouseout="staff.showActions = false"
      class="card card-body mb-3"
    >
      <StaffForm
        v-if="
          staff.action === 'update' && staff.itemId === item['id'].toString()
        "
        :staff="staff.item"
        @submit="submitForm"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="staff.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'staffs')"
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
</template>
