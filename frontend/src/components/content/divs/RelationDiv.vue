<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Relation } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
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

onBeforeMount(async () => {
  await stateAnketa.getItem("relations");
});

const relation = ref({
  action: "",
  itemId: "",
  item: <Relation>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(
    relation.value.action,
    "relations",
    relation.value.itemId,
    form
  );
  
  relation.value.action = "";
  relation.value.itemId = "";
}
</script>

<template>
  <ActionHeader
    :id="'relation'"
    :header="'Связи'"
    :action="relation.action"
    @action="relation.action = relation.action ? '' : 'create'"
  />
  <RelationForm
    v-if="relation.action === 'create'"
    @submit="submitForm"
    @cancel="
      relation.action = '';
      relation.itemId = '';
    "
  />
  <div
    v-if="stateAnketa.anketa.relations.length"
    class="collapse show"
    id="relation"
  >
    <div
      v-for="(item, idx) in stateAnketa.anketa.relations"
      :key="idx"
      class="card card-body mb-3"
      @mouseover="relation.showActions = true"
      @mouseout="relation.showActions = false"
    >
      <RelationForm
        v-if="
          relation.action === 'update' &&
          relation.itemId === item['id'].toString()
        "
        :relation="relation.item"
        @submit="submitForm"
        @cancel="
          relation.action = '';
          relation.itemId = '';
        "
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="relation.showActions"
            :hide="true"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'relations')"
            @update="
              relation.action = 'update';
              relation.item = item;
              relation.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'Тип'">{{ item["relation"] }}</LabelSlot>
        <LabelSlot :label="'Связь'" :no-print="true">
          <router-link
            :to="{
              name: 'profile',
              params: { id: String(item['relation_id']) },
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
