<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Needs } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const InquiryForm = defineAsyncComponent(
  () => import("@components/content/forms/InquiryForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/elements/LabelValue.vue")
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
  emit(
    "submit", 
    need.value.action, 
    "inquiry", 
    need.value.itemId, 
    form
  );
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
          :idx="idx.toString()"
          :label="'Запрос #' + (idx + 1)"
        >
          <LabelValue :label="'Действия'">
            <a
              href="#"
              title="Удалить"
              @click="emit('delete', item['id'].toString(), 'inquiry')"
            >
              <i class="bi bi-trash"></i>
            </a>
            &nbsp;
            <a
              href="#"
              title="Изменить"
              @click="
                need.action = 'update';
                need.item = props.needs[idx];
                need.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </LabelValue>
          <LabelValue :label="'ID'">{{ item["id"] }}</LabelValue>
          <LabelValue :label="'Информация'">{{ item["info"] }}</LabelValue>
          <LabelValue :label="'Иннициатор'">{{ item["initiator"] }}</LabelValue>
          <LabelValue :label="'Источник'">{{ item["source"] }}</LabelValue>
          <LabelValue :label="'Сотрудник'">{{ item["officer"] }}</LabelValue>
          <LabelValue :label="'Дата запроса'">
            {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
          </LabelValue>
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
