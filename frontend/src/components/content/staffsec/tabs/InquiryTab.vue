<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount, computed } from "vue";
import { Needs } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/CollapseDiv.vue")
);
const InquiryForm = defineAsyncComponent(
  () => import("../forms/InquiryForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
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

const inquiryObject = computed(() => {
  return props.needs.map((item) => ({
    id: ["ID", item["id"]],
    theme: ["Информация", item["info"]],
    innitivator: ["Иннициатор", item["initiator"]],
    source: ["Источник", item["source"]],
    officer: ["Сотрудник", item["officer"]],
    deadline: [
      "Дата запроса", new Date(String(item['deadline'])).toLocaleDateString('ru-RU')
    ]
  }))
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
      <div v-if="inquiryObject.length">
        <CollapseDiv
          v-for="(item, idx) in inquiryObject"
          :key="idx"
          :id="'inquiry' + idx"
          :idx="idx.toString()"
          :label="'Запрос #' + (idx + 1)"
        >
          <LabelValue :label="'Действия'">
            <a
              href="#"
              title="Удалить"
              @click="emit('delete', item.id[1].toString(), 'inquiry')"
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
                need.itemId = item.id[1].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </LabelValue>
          <LabelValue 
            v-for="(value, key) in item" 
            :key="key"
            :label="value[0]"
          >
            {{ value[1] }}
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
