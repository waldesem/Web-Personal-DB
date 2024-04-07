<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Needs } from "@/interfaces/interface";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const InquiryForm = defineAsyncComponent(
  () => import("@components/content/forms/InquiryForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item", "inquiry");
});

const props = defineProps({
  needs: {
    type: Array as () => Array<Needs>,
    default: () => [],
  },
});

const need = ref({
  action: "",
  itemId: "",
  item: <Needs>{},
  showActions: false,
  handleMouse() {
    this.showActions = !this.showActions
  }
});

function submitForm(form: Object) {
  emit("submit", need.value.action, "inquiry", need.value.itemId, form);
  need.value.action = "";
  need.value.showActions = false;
};
</script>

<template>
  <div class="py-3">
    <InquiryForm v-if="need.action"
      :inquiry="need.item" 
      @submit="submitForm"
      @cancel="need.action = ''; need.showActions = false"
    />
    <div v-else
      @mouseover="need.handleMouse"
      @mouseout="need.handleMouse"
    >
      <div v-if="props.needs.length"> 
        <div class="mb-3" v-for="(item, idx) in props.needs" :key="idx">
          <div class="card card-body">
            <LabelSlot v-show="need.showActions">
              <ActionIcons
                @delete="emit('delete', item['id'].toString(), 'inquiry')"
                @update="
                  need.action = 'update';
                  need.item = item;
                  need.itemId = item['id'].toString();
                "
              />
            </LabelSlot>
            <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
            <LabelSlot :label="'Иннициатор'">{{ item["initiator"] }}</LabelSlot>
            <LabelSlot :label="'Источник'">{{ item["source"] }}</LabelSlot>
            <LabelSlot :label="'Сотрудник'">{{ item["officer"] }}</LabelSlot>
            <LabelSlot :label="'Дата запроса'">
              {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
            </LabelSlot>
          </div>
        </div>
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="need.action = 'create'"
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
