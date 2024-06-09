<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Inquisition } from "@/interfaces";
import { stateAnketa } from "@/state";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const InvestigationForm = defineAsyncComponent(
  () => import("@components/content/forms/InvestigationForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(async() => {
  await stateAnketa.getItem("investigations");
});

const emit = defineEmits(["cancel"]);

const props = defineProps({
  tabAction: {
    type: String,
    default: "",
  },
  currentTab: {
    type: String,
    default: "",
  }
})

const inquisition = ref({
  itemId: "",
  item: <Inquisition>{},
  showActions: false,
});

function submitForm(form: Object, action: string) {
  stateAnketa.updateItem(
    action,
    "investigations",
    inquisition.value.itemId,
    form
  );  
  action === "update" ? inquisition.value.itemId = "" : emit("cancel");
}
</script>

<template>
  <InvestigationForm
    v-if="props.tabAction === 'create' && props.currentTab === 'InvestigateTab'"
    :action="'create'"
    @submit="submitForm"
    @cancel="emit('cancel')"
  />
  <div v-else-if="stateAnketa.anketa.investigations.length" class="py-3"> 
    <div 
      v-for="(item, idx) in stateAnketa.anketa.investigations" :key="idx"
      class="mb-3"
      :class="{ 'card card-body': !stateAnketa.share.printPage }"
      @mouseover="inquisition.showActions = true"
      @mouseout="inquisition.showActions = false"
    >
      <InvestigationForm
        v-if="inquisition.itemId === item['id'].toString()"
        :poligraf="inquisition.item"
        :action="'update'"
        @submit="submitForm"
        @cancel="inquisition.itemId = ''"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons v-show="inquisition.showActions"
            :show-form="true"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'investigations')"
            @update="
              inquisition.item = item;
              inquisition.itemId = item['id'].toString();
            "
          >
          <FileForm 
            v-show="inquisition.showActions" 
            :accept="'*'" 
            @submit="stateAnketa.submitFile($event, 'investigation')" 
          />
          </ActionIcons>
        </LabelSlot>
        <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
        <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата'">
          {{ new Date(String(item["created"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot v-if="item['updated']" :label="'Обновлено'">
          {{ new Date(String(item["updated"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
