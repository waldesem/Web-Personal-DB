<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa, stateUser } from "@/state";
import { Relation } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const RelationForm = defineAsyncComponent(
  () => import("@components/content/forms/RelationForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

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
  <DropDownHead :id="'relationer'" :header="'Связи'" />
  <div class="collapse card card-body mb-3" id="relationer">
    <RelationForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.relations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.relations"
      :key="idx"
      class="card card-body mb-3"
      @mouseover="actions = true"
      @mouseout="actions = false"
    >
      <RelationForm
        v-if="edit && itemId == item['id'].toString()" 
        :relation="relation"
        @cancel="edit = !edit"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="
                actions &&
                stateAnketa.anketa.persons['user_id'] == stateUser.userId
              "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'relations')"
            @update="
              relation = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Тип'">{{ item["relation"] }}</LabelSlot>
        <LabelSlot :label="'Связь'">
          <router-link
            :to="{
              name: 'profile',
              params: { id: item['relation_id'] },
            }"
          >
            ID #{{ item["relation_id"] }}
          </router-link>
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
