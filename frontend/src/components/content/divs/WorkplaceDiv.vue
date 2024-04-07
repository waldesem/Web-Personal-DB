<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Work } from "@/interfaces/interface";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
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

onBeforeMount(() => {
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
    :id="'work'"
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
    @mouseover="workplace.showActions = true"
    @mouseout="workplace.showActions = false"
  >
    <div v-if="props.items.length" class="collapse" id="work"> 
      <div class="mb-3" v-for="(item, idx) in props.items" :key="idx">
        <div class="card card-body">
          <LabelSlot>
            <ActionIcons v-show="workplace.showActions"
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
        </div>
      </div>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
