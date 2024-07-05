<script setup lang="ts">
import { defineAsyncComponent, reactive, ref } from "vue";
import { stateAnketa, stateUser } from "@/state";
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

const actions = ref(false);
const itemId = ref('');
const edit = ref(false);
const doc = reactive(<Document>{});

function cancelAction(){
  edit.value = false;
  itemId.value = "";
  const collapseDocument = document.getElementById('documenter');
  collapseDocument?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <DropDownHead :id="'documenter'" :header="'Документы'"/>
  <div class="collapse card card-body mb-3" id="documenter">
    <DocumentForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.documents.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.documents"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <DocumentForm
        v-if="edit && itemId == item['id'].toString()" 
        :docs="doc"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="
                actions &&
                stateAnketa.anketa.persons['user_id'] == stateUser.userId
              "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'documents')"
            @update="
              doc = item;
              itemId = item['id'].toString()
              edit  = true;
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Вид документа'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Номер документа'">{{ item["digits"] }}</LabelSlot>
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