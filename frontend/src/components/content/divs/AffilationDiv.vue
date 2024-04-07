<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Affilation } from "@/interfaces/interface";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/content/forms/AffilationForm.vue")
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
    type: Array as () => Array<Affilation>,
    default: {},
  },
});

const affilation = ref({
  action: "",
  itemId: "",
  item: <Affilation>{},
  showActions: false,
  handleMouse() {
    this.showActions = !this.showActions;
  }

});

function submitForm(form: Object) {
  emit(
    "submit",
    affilation.value.action,
    "affilation",
    affilation.value.itemId,
    form
  );
  affilation.value.action = "";
  affilation.value.showActions = false;
}
</script>

<template>
  <ActionHeader
    :header="'Аффилированность'"
    :action="affilation.action"
    @action="affilation.action = affilation.action ? '' : 'create'"
  />
  <AffilationForm
    v-if="affilation.action"
    :affils="affilation.item"
    @submit="submitForm"
    @cancel="affilation.action = ''; affilation.showActions = false"
  />
  <div v-else
    @mouseover="affilation.handleMouse"
    @mouseout="affilation.handleMouse"
  >
    <div v-if="props.items.length" class="collapse" id="staff"> 
      <div class="mb-3" v-for="(item, idx) in props.items" :key="idx">
        <div class="card card-body">
          <LabelSlot v-show="affilation.showActions">
            <ActionIcons
              @delete="emit('delete', item['id'].toString(), 'affilation')"
              @update="
                affilation.action = 'update';
                affilation.item = item;
                affilation.itemId = item['id'].toString();
              "
            />
          </LabelSlot>
          <LabelSlot :label="'Тип участия'">{{ item["view"] }}</LabelSlot>
          <LabelSlot :label="'Организация'">{{ item["name"] }}</LabelSlot>
          <LabelSlot :label="'ИНН'">{{ item["inn"] }}</LabelSlot>
          <LabelSlot :label="'Должность'">{{ item["position"] }}</LabelSlot>
          <LabelSlot :label="'Дата декларации'">
            {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
          </LabelSlot>
        </div>
      </div>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
