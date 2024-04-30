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
  stateAnketa.getItem("workplace");
});

const workplace = ref({
  action: "",
  itemId: "",
  item: <Work>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(
    workplace.value.action,
    "workplace",
    workplace.value.itemId,
    form
  );
  
  workplace.value.action = "";
  workplace.value.itemId = "";
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
    @cancel="
      workplace.action = '';
      workplace.itemId = '';
    "
  />
  <div
    v-if="stateAnketa.anketa.workplace.length"
    :class="{ 'collapse show': !stateAnketa.share.printPage }"
    id="work"
  >
    <div
      class="mb-3"
      v-for="(item, idx) in stateAnketa.anketa.workplace"
      :key="idx"
      @mouseover="workplace.showActions = true"
      @mouseout="workplace.showActions = false"
      :class="{ 'card card-body': !stateAnketa.share.printPage }"
    >
      <WorkplaceForm
        v-if="
          workplace.action === 'update' &&
          workplace.itemId === item['id'].toString()
        "
        :work="workplace.item"
        @submit="submitForm"
        @cancel="
          workplace.action = '';
          workplace.itemId = '';
        "
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="workplace.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'workplace')"
            @update="
              workplace.action = 'update';
              workplace.item = item;
              workplace.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'ID'">
          {{ item["id"] }}
        </LabelSlot>
        <LabelSlot v-if="!item['end_date']" :label="'Текущая работа'">
          {{ item["now_work"] }}
        </LabelSlot>
        <LabelSlot :label="'Начало работы'">
          {{ item["start_date"] }}
        </LabelSlot>
        <LabelSlot v-if="!item['now_work']" :label="'Окончание работы'">
          {{ item["end_date"] }}
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
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
