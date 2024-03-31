<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Staff } from "@/interfaces/interface";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
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

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item", "staff");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Staff>,
    default: {},
  },
});

const staff = ref({
  action: "",
  itemId: "",
  item: <Staff>{},
});

function submitForm(form: Object) {
  emit("submit", staff.value.action, "staff", staff.value.itemId, form);
  staff.value.action = "";
}
</script>

<template>
  <ActionHeader
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
  <div v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'staff' + idx"
        :idx="idx.toString()"
        :label="'Должность #' + (idx + 1)"
      >
        <LabelSlot :label="'Действия'" :no-print="true">
          <ActionIcons
            @delete="emit('delete', item['id'].toString(), 'staff')"
            @update="
              staff.action = 'update';
              staff.item = item;
              staff.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'ID'">{{ item["id"] }}</LabelSlot>
        <LabelSlot :label="'Должность'">{{ item["position"] }}</LabelSlot>
        <LabelSlot :label="'Департамент'">{{ item["department"] }}</LabelSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
