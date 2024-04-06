<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Document } from "@/interfaces/interface";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const DocumentForm = defineAsyncComponent(
  () => import("@components/content/forms/DocumentForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(async() => {
  emit("get-item");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Document>,
    default: {},
  },
});

const document = ref({
  action: "",
  itemId: "",
  item: <Document>{},
});

function submitForm(form: Object) {
  emit("submit", document.value.action, "document", document.value.itemId, form)
  document.value.action = '';
};
</script>

<template>
  <ActionHeader
    :header="'Документы'"
    :action="document.action"
    @action="document.action = document.action ? '' : 'create'"
  />
  <DocumentForm v-if="document.action"
    :docs="document.item"
    @submit="submitForm"
    @cancel="document.action = ''"
  />
  <div v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'docum' + idx"
        :idx="idx.toString()"
        :label="'Документ #' + (idx + 1)"
      >
        <LabelSlot :label="'Действия'" :no-print="true">
          <ActionIcons
            @delete="emit('delete', item['id'].toString(), 'document')"
            @update="
              document.action = 'update';
              document.item = item;
              document.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'ID'">{{ item['id'] }}</LabelSlot>
        <LabelSlot :label="'Вид документа'">{{ item['view'] }}</LabelSlot>
        <LabelSlot :label="'Номер документа'">{{ item['number'] }}</LabelSlot>
        <LabelSlot :label="'Серия документа'">{{ item['series'] }}</LabelSlot>
        <LabelSlot :label="'Кем выдан'">{{ item['agency'] }}</LabelSlot>
        <LabelSlot :label="'Дата выдачи'">
          {{ new Date(String(item['issue'])).toLocaleDateString('ru-RU') }}
        </LabelSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
