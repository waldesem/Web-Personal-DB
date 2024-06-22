<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Inquisition } from "@/interfaces";
import { stateAnketa, submitFile } from "@/state";

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
  spinner: false
});

function cancelAction(){
  inquisition.value.itemId = "";
  inquisition.value.item = <Inquisition>({});
  emit("cancel");
};

function submitForm(form: Object) {
  stateAnketa.updateItem(
    "investigations",
    form
  );  
  cancelAction();
};

function uploadInquisitionFile(event: Event) {
  inquisition.value.spinner = true;
  submitFile(event, "investigations");
  inquisition.value.spinner = false;
};
</script>

<template>
  <InvestigationForm
    v-if="props.tabAction === 'create' && props.currentTab === 'InvestigateTab'"
    @submit="submitForm"
    @cancel="emit('cancel')"
  />
  <div v-else-if="stateAnketa.anketa.investigations.length" class="py-3"> 
    <div 
      v-for="(item, idx) in stateAnketa.anketa.investigations" :key="idx"
      @mouseover="inquisition.showActions = true"
      @mouseout="inquisition.showActions = false"
      class="card card-body mb-3"
    >
      <InvestigationForm
        v-if="inquisition.itemId === item['id'].toString()"
        :investigation="inquisition.item"
        @submit="submitForm"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons v-show="inquisition.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'investigations')"
            @update="
              inquisition.item = item;
              inquisition.itemId = item['id'].toString();
            "
            :for-input="'investigations-file'"
          >
            <span v-if="inquisition.spinner" class="spinner-border-sm text-primary"></span>
            <FileForm 
              v-show="inquisition.showActions" 
              :name-id="'investigations-file'"
              :accept="'*'" 
              @submit="uploadInquisitionFile($event)" 
            />
          </ActionIcons>  
        </LabelSlot>
        <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
        <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(String(item["created"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
