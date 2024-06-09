<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Needs } from "@/interfaces";
import { stateAnketa } from "@/state";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const InquiryForm = defineAsyncComponent(
  () => import("@components/content/forms/InquiryForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(async() => {
  await stateAnketa.getItem("inquiries");
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

const need = ref({
  itemId: "",
  item: <Needs>{},
  showActions: false,
});

function submitForm(form: Object, action: string) {
  stateAnketa.updateItem(action, "inquiries", need.value.itemId, form);
  need.value.itemId = "";
  action === "update" ? need.value.itemId = "" : emit("cancel");
};
</script>

<template>
  <InquiryForm v-if="props.tabAction === 'create' && props.currentTab === 'InquiryTab'"
    @submit="submitForm"
    @cancel="emit('cancel')"
  />
  <div v-else-if="stateAnketa.anketa.inquiries.length" class="py-3"> 
    <div
      class="mb-3"
      v-for="(item, idx) in stateAnketa.anketa.inquiries" :key="idx"
      @mouseover="need.showActions = true"
      @mouseout="need.showActions = false" 
      :class="{ 'card card-body': !stateAnketa.share.printPage }"
    >
      <InquiryForm
        v-if="need.itemId === item['id'].toString()"
        :poligraf="need.item"
        :action="'update'"
        @submit="submitForm"
        @cancel="need.itemId = ''"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons v-show="need.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'inquiries')"
            @update="
              need.item = item;
              need.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
        <LabelSlot :label="'Иннициатор'">{{ item["initiator"] }}</LabelSlot>
        <LabelSlot :label="'Источник'">{{ item["source"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата запроса'">
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
