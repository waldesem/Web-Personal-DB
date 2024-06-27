<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
import { Previous } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const PreviousForm = defineAsyncComponent(
  () => import("@components/content/forms/PreviousForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const previous = ref({
  itemId: "",
  item: <Previous>{},
  showActions: false,
});

function cancelAction(){
  previous.value.itemId = "";
  Object.keys(previous.value.item).forEach(
    (key) => delete previous.value.item[key as keyof typeof previous.value.item]
  );
  const collapsePrevious = document.getElementById('previous');
  collapsePrevious?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <DropDownHead :id="'previous'" :header="'Изменение имени'"/>
  <div class="collapse card card-body mb-3" id="previous">
    <PreviousForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.previous.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.previous"
      :key="idx"
      @mouseover="previous.showActions = true"
      @mouseout="previous.showActions = false"
      class="card card-body mb-3"
    >
      <PreviousForm
        v-if="previous.itemId === item['id'].toString()"
        :previous="previous.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="previous.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'previous')"
            @update="
              previous.item = item;
              previous.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Фамилия'">
          {{ item["surname"] }}
        </LabelSlot>
        <LabelSlot :label="'Имя'">
          {{ item["firstname"] }}
        </LabelSlot>
        <LabelSlot v-if="item['patronymic']" :label="'Отчество'">
          {{ item["patronymic"] }}
        </LabelSlot>
        <LabelSlot v-if="item['changed']" :label="'Дата изменения'">
          {{
            new Date(String(item["changed"])).toLocaleDateString("ru-RU")
          }}
        </LabelSlot>
        <LabelSlot v-if="item['reason']" :label="'Причина'">
          {{ item["reason"] }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>