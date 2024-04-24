<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Inquisition } from "@/interfaces";
import { stateClassify, stateAnketa } from "@/state";

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
  await stateAnketa.getItem("investigation");
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
  action: "",
  itemId: "",
  item: <Inquisition>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(
    inquisition.value.action,
    "investigation",
    inquisition.value.itemId,
    form
  );
  
  inquisition.value.action = "";
  inquisition.value.itemId = "";
  emit("cancel");
}
</script>

<template>
  <InvestigationForm
    v-if="props.tabAction === 'create' && props.currentTab === 'InvestigateTab'"
    @submit="submitForm"
    @cancel="inquisition.action = ''; inquisition.itemId = ''; emit('cancel')"
  />
  <div v-if="stateAnketa.anketa.investigation.length"> 
    <div 
      v-for="(item, idx) in stateAnketa.anketa.investigation" :key="idx"
      class="mb-3"
      :class="{ 'card card-body': !stateAnketa.share.printPage }"
      @mouseover="inquisition.showActions = true"
      @mouseout="inquisition.showActions = false"
    >
      <LabelSlot>
        <ActionIcons v-show="inquisition.showActions"
          :show-form="true"
          @delete="stateAnketa.deleteItem(item['id'].toString(), 'investigation')"
          @update="
            inquisition.action = 'update';
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
      <LabelSlot :label="'Сотрудник'">{{ stateClassify.users[item["user_id"]] }}</LabelSlot>
      <LabelSlot :label="'Дата'">
        {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
      </LabelSlot>

    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
