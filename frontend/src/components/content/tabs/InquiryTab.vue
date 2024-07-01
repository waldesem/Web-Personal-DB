<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Needs } from "@/interfaces";
import { stateAnketa } from "@/state";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const InquiryForm = defineAsyncComponent(
  () => import("@components/content/forms/InquiryForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const need = ref({
  itemId: "",
  item: <Needs>{},
  showActions: false,
});

function cancelAction(){
  need.value.itemId = "";
  Object.keys(need.value.item).forEach(
    (key) => delete need.value.item[key as keyof typeof need.value.item]
  );
  const collapseInquiry = document.getElementById('inquiry');
  collapseInquiry?.setAttribute('class', 'collapse card card-body');
};
</script>

<template>
  <div class="collapse card card-body" id="inquiry">
    <InquiryForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.inquiries.length"> 
    <div
      class="card card-body"
      v-for="(item, idx) in stateAnketa.anketa.inquiries" :key="idx"
      @mouseover="need.showActions = true"
      @mouseout="need.showActions = false" 
    >
      <InquiryForm
        v-if="need.itemId === item['id'].toString()"
        :inquiry="need.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons v-show="need.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'inquiries')"
            @update="
              need.item = item;
              need.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Запросы о сотруднике #" + (idx+1) }}
        </p>
        <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
        <LabelSlot :label="'Иннициатор'">{{ item["initiator"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + ' UTC').toLocaleString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p class="p-3" v-else>Запросы о сотруднике не поступали</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>