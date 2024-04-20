<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Relation } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const RelationForm = defineAsyncComponent(
  () => import("@components/content/forms/RelationForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item");
});

const props = defineProps({
  printPage: {
    type: Boolean,
    default: false,
  },
});

const relation = ref({
  action: "",
  itemId: "",
  item: <Relation>{},
  showActions: false,
});

function submitForm(form: Object) {
  emit("submit", 
    relation.value.action,
    "relation",
    relation.value.itemId,
    form,
  );
  relation.value.action = "";
};
</script>

<template>
  <ActionHeader
    :print-page="props.printPage"
    :id="'relation'"
    :header="'Связи'"
    :action="relation.action"
    @action="relation.action = relation.action ? '' : 'create'"
  />
  <RelationForm v-if="relation.action"
    :content="relation.item"
    @submit="submitForm"
    @cancel="relation.action = ''"
  />
  <div v-else
    @mouseover="relation.showActions = true"
    @mouseout="relation.showActions = false"
  >
    <div 
      v-if="stateAnketa.relation.length" 
      :class="{'collapse show': !printPage}" 
      id="relation"
    > 
      <div class="mb-3" v-for="(item, idx) in stateAnketa.relation" :key="idx">
        <div class="card card-body">
          <LabelSlot>
            <ActionIcons v-show="relation.showActions"
              @delete="emit('delete', item['id'].toString(), 'relation')"
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
  </div>
</template>
