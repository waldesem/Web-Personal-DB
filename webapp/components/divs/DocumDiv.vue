<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Document } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

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
  <div v-if="anketaState.anketa.value.documents.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.documents"
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
                anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
                anketaState.anketa.value.persons['standing']
              "
            @delete="anketaState.deleteItem(item['id'].toString(), 'documents')"
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