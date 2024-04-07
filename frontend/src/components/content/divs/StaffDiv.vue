<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Staff } from "@/interfaces/interface";

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

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item");
});

const props = defineProps({
  items: {
    type: Array<Staff>,
    default: [{}],
  },
});

const staff = ref({
  action: "",
  itemId: "",
  item: <Staff>{},
  showActions: false,
  handleMouse() {
    this.showActions = !this.showActions;
  }
});

function submitForm(form: Object) {
  emit("submit", staff.value.action, "staff", staff.value.itemId, form);
  staff.value.action = "";
  staff.value.showActions = false;
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
    @cancel="staff.action = ''; staff.showActions = false"
  />
  <div v-else
    @mouseover="staff.handleMouse"
    @mouseout="staff.handleMouse"
  >
    <div v-if="props.items.length" class="collapse" id="staff"> 
      <div class="mb-3" v-for="(item, idx) in props.items" :key="idx">
        <div class="card card-body">
          <LabelSlot v-show="staff.showActions">
            <ActionIcons
              @delete="emit('delete', item['id'].toString(), 'staff')"
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
