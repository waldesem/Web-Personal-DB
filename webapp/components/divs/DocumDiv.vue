<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "../../utils/state";
import type { Document } from "../../utils/interfaces";

const actions = ref(false);
const itemId = ref('');
const edit = ref(false);
const doc = ref(<Document>{});

function cancelAction(){
  edit.value = false;
  itemId.value = "";
  const collapseDocument = document.getElementById('documenter');
  collapseDocument?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <ElementsDropDownHead :id="'documenter'" :header="'Документы'"/>
  <div class="collapse card card-body mb-3" id="documenter">
    <FormsDocumentForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.documents.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.documents"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <FormsDocumentForm
        v-if="edit && itemId == item['id'].toString()" 
        :docs="doc"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
                actions &&
                stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
                stateAnketa.anketa.persons['standing']
              "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'documents')"
            @update="
              doc = item;
              itemId = item['id'].toString()
              edit  = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Вид документа'">{{ item["view"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Номер документа'">{{ item["digits"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Серия документа'">{{ item["series"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата выдачи'">
          {{ item["issue"] ? new Date(String(item["issue"])).toLocaleDateString("ru-RU") : '' }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Кем выдан'">{{ item["agency"] }}</ElementsLabelSlot>
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