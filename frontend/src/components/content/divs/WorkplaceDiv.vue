<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Work } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/content/forms/WorkplaceForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(() => {
  stateAnketa.getItem("workplaces");
});

const workplace = ref({
  action: "",
  itemId: "",
  item: <Work>{},
  showActions: false,
});

function cancelAction(){
  workplace.value.action = "";
  workplace.value.itemId = "";
  workplace.value.item = <Work>({});
};

function submitForm(form: Object) {
  stateAnketa.updateItem(
    "workplaces",
    form
  );
  cancelAction();
}
</script>

<template>
  <ActionHeader
    :id="'work'"
    :header="'Работа'"
    :action="workplace.action"
    @action="workplace.action = workplace.action ? '' : 'create'"
  />
  <WorkplaceForm
    v-if="workplace.action === 'create'"
    @submit="submitForm"
    @cancel="cancelAction"
  />
  <div
    v-if="stateAnketa.anketa.workplaces.length"
    class="collapse show"
    id="work"
  >
    <div
      v-for="(item, idx) in stateAnketa.anketa.workplaces"
      :key="idx"
      @mouseover="workplace.showActions = true"
      @mouseout="workplace.showActions = false"
      class="card card-body mb-3"
    >
      <WorkplaceForm
        v-if="
          workplace.action === 'update' &&
          workplace.itemId === item['id'].toString()
        "
        :work="workplace.item"
        @submit="submitForm"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="workplace.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'workplaces')"
            @update="
              workplace.action = 'update';
              workplace.item = item;
              workplace.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot v-if="item['now_work']" :label="'Текущая работа'">
          {{ item["now_work"] ? "Да" : "Нет" }}
        </LabelSlot>
        <LabelSlot :label="'Начало работы'">
          {{ new Date(item["started"]).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot v-if="!item['now_work']" :label="'Окончание работы'">
          {{ new Date(item["finished"]).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot :label="'Место работы'">
          {{ item["workplace"] }}
        </LabelSlot>
        <LabelSlot :label="'Адрес'">
          {{ item["address"] }}
        </LabelSlot>
        <LabelSlot :label="'Должность'">
          {{ item["position"] }}
        </LabelSlot>
        <LabelSlot :label="'Причина увольнения'">
          {{ item["reason"] }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
