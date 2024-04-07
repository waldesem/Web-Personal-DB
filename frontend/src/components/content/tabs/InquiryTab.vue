<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Needs } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
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

onBeforeMount(async () => {
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
});

function submitForm(form: Object) {
  emit("submit", need.value.action, "inquiry", need.value.itemId, form);
  need.value.action = "";
};
</script>

<template>
  <div class="py-3">
    <InquiryForm v-if="need.action"
      :inquiry="need.item" 
      @submit="submitForm"
      @cancel="need.action = ''"
    />
    <div v-else>
      <div v-if="props.needs.length">
        <CollapseDiv
          v-for="(item, idx) in props.needs"
          :key="idx"
          :id="'inquiry' + idx"
          :label="'Запрос #' + (idx + 1)"
        >
          <LabelSlot :label="'Действия'">
            <ActionIcons
              @delete="emit('delete', item['id'].toString(), 'inquiry')"
              @update="
                need.action = 'update';
                need.item = item;
                need.itemId = item['id'].toString();
              "
            />
          </LabelSlot>
          <LabelSlot :label="'ID'">{{ item["id"] }}</LabelSlot>
          <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
          <LabelSlot :label="'Иннициатор'">{{ item["initiator"] }}</LabelSlot>
          <LabelSlot :label="'Источник'">{{ item["source"] }}</LabelSlot>
          <LabelSlot :label="'Сотрудник'">{{ item["officer"] }}</LabelSlot>
          <LabelSlot :label="'Дата запроса'">
            {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
          </LabelSlot>
        </CollapseDiv>
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
