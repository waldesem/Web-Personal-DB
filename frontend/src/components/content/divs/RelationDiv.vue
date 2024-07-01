<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
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

const relation = ref({
  itemId: "",
  item: <Relation>{},
  showActions: false,
});

function cancelAction(){
  relation.value.itemId = "";
  Object.keys(relation.value.item).forEach(
    (key) => delete relation.value.item[key as keyof typeof relation.value.item]
  );
  const collapseRelation = document.getElementById('relation');
  collapseRelation?.setAttribute('class', 'collapse card card-body');
};
</script>

<template>
  <DropDownHead :id="'relation'" :header="'Связи'"/>
  <div class="collapse card card-body" id="relation">
    <RelationForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.relations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.relations"
      :key="idx"
      class="card card-body"
      @mouseover="relation.showActions = true"
      @mouseout="relation.showActions = false"
    >
      <RelationForm
        v-if="relation.itemId === item['id'].toString()"
        :relation="relation.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="relation.showActions"
            :hide="true"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'relations')"
            @update="
              relation.item = item;
              relation.itemId = item['id'].toString();
            "
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