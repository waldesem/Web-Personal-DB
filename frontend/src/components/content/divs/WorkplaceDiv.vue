<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Work } from "@/interfaces/interface";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/content/forms/WorkplaceForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(async() => {
  emit("get-item");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Work>,
    default: {},
  },
});

const workplace = ref({
  action: "",
  itemId: "",
  item: <Work>{},
  showActions: false,
  handleMouse() {
    this.showActions = !this.showActions;
  }
});

function submitForm(form: Object) {
  emit(
    "submit", 
    workplace.value.action,
    "workplace",
    workplace.value.itemId,
    form,
  );
  workplace.value.action = "";
};
</script>

<template>
  <ActionHeader
    :header="'Работа'"
    :action="workplace.action"
    @action="workplace.action = workplace.action ? '' : 'create'"
  />
  <WorkplaceForm v-if="workplace.action"
    :content="workplace.item"
    @submit="submitForm"
    @cancel="workplace.action = ''"
  />
  <div v-else
    @mouseover="workplace.handleMouse"
    @mouseout="workplace.handleMouse"
  >
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'work' + idx"
        :label="'Работа #' + (idx + 1)"
      >
        <LabelSlot v-show="workplace.showActions">
          <ActionIcons
            @delete="emit('delete', item['id'].toString(), 'workplace')"
            @update="
              workplace.action = 'update';
              workplace.item = item;
              workplace.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'ID'">{{ item['id'] }}</LabelSlot>
        <LabelSlot :label="'Начало работы'">{{ item['start_date'] }}</LabelSlot>
        <LabelSlot :label="'Окончание работы'">{{ item['end_date'] }}</LabelSlot>
        <LabelSlot :label="'Место работы'">{{ item['workplace'] }}</LabelSlot>
        <LabelSlot :label="'Адрес'">{{ item['address'] }}</LabelSlot>
        <LabelSlot :label="'Должность'">{{ item['position'] }}</LabelSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
