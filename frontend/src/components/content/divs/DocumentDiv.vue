<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
import { Document } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const DocumentForm = defineAsyncComponent(
  () => import("@components/content/forms/DocumentForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const doc = ref({
  itemId: "",
  item: <Document>{},
  showActions: false,
});

function cancelAction(){
  doc.value.itemId = "";
  Object.keys(doc.value.item).forEach(
    (key) => delete doc.value.item[key as keyof typeof doc.value.item]
  );
  const collapseDocument = document.getElementById('document');
  collapseDocument?.setAttribute('class', 'collapse card card-body');
};
</script>

<template>
  <DropDownHead :id="'document'" :header="'Документы'"/>
  <div class="collapse card card-body" id="document">
    <DocumentForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.documents.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.documents"
      :key="idx"
      @mouseover="doc.showActions = true"
      @mouseout="doc.showActions = false"
      class="card card-body"
    >
      <DocumentForm
        v-if="doc.itemId === item['id'].toString()"
        :docs="doc.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="doc.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'documents')"
            @update="
              doc.item = item;
              doc.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Вид документа'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Номер документа'">{{ item["number"] }}</LabelSlot>
        <LabelSlot :label="'Серия документа'">{{ item["series"] }}</LabelSlot>
        <LabelSlot :label="'Дата выдачи'">
          {{ new Date(String(item["issue"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot :label="'Кем выдан'">{{ item["agency"] }}</LabelSlot>
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