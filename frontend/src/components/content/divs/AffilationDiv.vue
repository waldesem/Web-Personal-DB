<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Affilation } from "@/interfaces";

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
  printPage: {
    type: Boolean,
    default: false,
  },
});

const affilation = ref({
  action: "",
  itemId: "",
  item: <Affilation>{},
  showActions: false,
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
}
</script>

<template>
  <ActionHeader
    :print-page="props.printPage"
    :header="'Аффилированность'"
    :action="affilation.action"
    @action="affilation.action = affilation.action ? '' : 'create'"
  />
  <AffilationForm
    v-if="affilation.action"
    :affils="affilation.item"
    @submit="submitForm"
    @cancel="affilation.action = ''"
  />
  <div v-else
    @mouseover="affilation.showActions = true"
    @mouseout="affilation.showActions = false"
  >
    <div 
      v-if="stateAnketa.affilation.length" 
      :class="{'collapse show': !printPage}" 
      id="affilation"
    > 
      <div class="mb-3" v-for="(item, idx) in stateAnketa.affilation" :key="idx">
        <div class="card card-body">
          <LabelSlot>
            <ActionIcons v-show="affilation.showActions"
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
