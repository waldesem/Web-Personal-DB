<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Document } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
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

onBeforeMount(async () => {
  await stateAnketa.getItem("document");
});

const document = ref({
  action: "",
  itemId: "",
  item: <Document>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(
    document.value.action,
    "document",
    document.value.itemId,
    form
  );
  document.value.action = "";
  document.value.itemId = "";
}
</script>

<template>
  <ActionHeader
    :id="'document'"
    :header="'Документы'"
    :action="document.action"
    @action="document.action = document.action ? '' : 'create'"
  />
  <DocumentForm
    v-if="document.action === 'create'"
    :docs="document.item"
    @submit="submitForm"
    @cancel="
      document.action = '';
      document.itemId = '';
    "
  />
  <div
    v-if="stateAnketa.anketa.document.length"
    :class="{ 'collapse show': !stateAnketa.share.printPage }"
    id="document"
  >
    <div
      class="mb-3"
      v-for="(item, idx) in stateAnketa.anketa.document"
      :key="idx"
      @mouseover="document.showActions = true"
      @mouseout="document.showActions = false"
      :class="{ 'card card-body': !stateAnketa.share.printPage }"
    >
      <DocumentForm
        v-if="
          document.action === 'update' &&
          document.itemId === item['id'].toString()
        "
        :docs="document.item"
        @submit="submitForm"
        @cancel="
          document.action = '';
          document.itemId = '';
        "
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="document.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'document')"
            @update="
              document.action = 'update';
              document.item = item;
              document.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'Вид документа'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Номер документа'">{{ item["number"] }}</LabelSlot>
        <LabelSlot :label="'Серия документа'">{{ item["series"] }}</LabelSlot>
        <LabelSlot :label="'Кем выдан'">{{ item["agency"] }}</LabelSlot>
        <LabelSlot :label="'Дата выдачи'">
          {{ new Date(String(item["issue"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
