<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Affilation } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/content/forms/AffilationForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(async () => {
  await stateAnketa.getItem("affilations");
});

const affilation = ref({
  action: "",
  itemId: "",
  item: <Affilation>{},
  showActions: false,
});

function cancelAction(){
  affilation.value.action = "";
  affilation.value.itemId = "";
  affilation.value.item = <Affilation>({});
};

function submitForm(form: Object) {
  stateAnketa.updateItem(
    "affilations",
    form
  );
  cancelAction();
}
</script>

<template>
  <ActionHeader
    :header="'Аффилированность'"
    :action="affilation.action"
    @action="affilation.action = affilation.action ? '' : 'create'"
  />
  <AffilationForm
    v-if="affilation.action === 'create'"
    :affils="affilation.item"
    @submit="submitForm"
    @cancel="cancelAction"
  />
  <div
    v-if="stateAnketa.anketa.affilations.length"
    class="collapse show"
    id="affilation"
  >
    <div
      v-for="(item, idx) in stateAnketa.anketa.affilations"
      :key="idx"
      @mouseover="affilation.showActions = true"
      @mouseout="affilation.showActions = false"
      class="card card-body mb-3"
    >
      <AffilationForm
        v-if="
          affilation.action === 'update' &&
          affilation.itemId === item['id'].toString()
        "
        :affils="affilation.item"
        @submit="submitForm"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="affilation.showActions"
            @delete="
              stateAnketa.deleteItem(item['id'].toString(), 'affilations')
            "
            @update="
              affilation.action = 'update';
              affilation.item = item;
              affilation.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Тип участия'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Организация'">{{ item["name"] }}</LabelSlot>
        <LabelSlot :label="'ИНН'">{{ item["inn"] }}</LabelSlot>
        <LabelSlot :label="'Должность'">{{ item["position"] }}</LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
