<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Needs } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const InquiryForm = defineAsyncComponent(
  () => import("../forms/InquiryForm.vue")
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
          <LabelSlot>
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
                need.item = item;
                need.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </LabelSlot>
          <LabelValue :label="'Информация'" :value="item['info']" />
          <LabelValue :label="'Иннициатор'" :value="item['initiator']" />
          <LabelValue :label="'Источник'" :value="item['source']" />
          <LabelValue :label="'Сотрудник'" :value="item['officer']" />
          <LabelValue :label="'Дата запроса'" :value="item['deadline']" />
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
