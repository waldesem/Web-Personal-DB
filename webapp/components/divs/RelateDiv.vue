<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Relation } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const edit = ref(false);
const itemId = ref('');
const relation = ref(<Relation>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapseRelation = document.getElementById("relationer");
  collapseRelation?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <ElementsDropDownHead :id="'relationer'" :header="'Связи'" />
  <div class="collapse card card-body mb-3" id="relationer">
    <FormsRelationForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.relations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.relations"
      :key="idx"
      class="card card-body mb-3"
      @mouseover="actions = true"
      @mouseout="actions = false"
    >
      <FormsRelationForm
        v-if="edit && itemId == item['id'].toString()" 
        :relation="relation"
        @cancel="edit = !edit"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
                actions &&
                anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
                anketaState.anketa.value.persons['standing']
              "
            @delete="anketaState.deleteItem(item['id'].toString(), 'relations')"
            @update="
              relation = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Тип'">{{ item["relation"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Связь'">
          <router-link
            :to="{
              name: 'profile',
              params: { id: item['relation_id'] },
            }"
          >
            ID #{{ item["relation_id"] }}
          </router-link>
        </ElementsLabelSlot>
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
