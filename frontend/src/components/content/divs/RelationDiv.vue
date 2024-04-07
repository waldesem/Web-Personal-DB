<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Relation } from "@/interfaces/interface";

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
  items: {
    type: Array as () => Array<Relation>,
    default: {},
  },
});

const relation = ref({
  action: "",
  itemId: "",
  item: <Relation>{},
  showActions: false,
  handleMouse() {
    this.showActions = !this.showActions;
  }
});

function submitForm(form: Object) {
  emit("submit", 
    relation.value.action,
    "relation",
    relation.value.itemId,
    form,
  );
  relation.value.action = "";
  relation.value.showActions = false;
};
</script>

<template>
  <ActionHeader
    :id="'relation'"
    :header="'Связи'"
    :action="relation.action"
    @action="relation.action = relation.action ? '' : 'create'"
  />
  <RelationForm v-if="relation.action"
    :content="relation.item"
    @submit="submitForm"
    @cancel="relation.action = ''; relation.showActions = false"
  />
  <div v-else
    @mouseover="relation.handleMouse"
    @mouseout="relation.handleMouse"
  >
    <div v-if="props.items.length" class="collapse" id="relation"> 
      <div class="mb-3" v-for="(item, idx) in props.items" :key="idx">
        <div class="card card-body">
          <LabelSlot v-show="relation.showActions">
            <ActionIcons
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
