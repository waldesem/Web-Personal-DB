<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
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

function cancelAction(){
  need.value.itemId = "";
  Object.keys(need.value.item).forEach(
    (key) => delete need.value.item[key as keyof typeof need.value.item]
  );  emit("cancel");
};

function submitForm(form: Object) {
  stateAnketa.updateItem(
    "inquiries", 
    form
  );
  cancelAction();
};
</script>

<template>
  <InquiryForm v-if="props.tabAction === 'create' && props.currentTab === 'InquiryTab'"
    @submit="submitForm"
    @cancel="emit('cancel')"
  />
  <div v-else-if="stateAnketa.anketa.inquiries.length" class="py-3"> 
    <div
      class="card card-body mb-3"
      v-for="(item, idx) in stateAnketa.anketa.inquiries" :key="idx"
      @mouseover="need.showActions = true"
      @mouseout="need.showActions = false" 
    >
      <InquiryForm
        v-if="need.itemId === item['id'].toString()"
        :inquiry="need.item"
        @submit="submitForm"
        @cancel="cancelAction"
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
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(String(item["created"])).toLocaleString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
