<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Affilation } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/AffilationForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(async () => {
  emit("get-item", "affilation");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Affilation>,
    default: {},
  },
});

const affilation = ref({
  action: "",
  itemId: "",
  item: <Affilation>{},
});

function submitForm(form: Object) {
  emit(
    "submit", 
    affilation.value.action,
    "affilation",
    affilation.value.itemId,
    form,
  );
  affilation.value.action = "";
};
</script>

<template>
  <h6>
    Аффилированность
    <a
      class="btn btn-link"
      @click="affilation.action = affilation.action ? '' : 'create'"
      title="Добавить информацию"
    >
      <i class="bi bi-plus-circle"></i>
    </a>
  </h6>
  <AffilationForm v-if="affilation.action"
    :affils="affilation.item" 
    @submit="submitForm" 
  />
  <div v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'affil' + idx"
        :idx="idx.toString()"
        :label="'Аффилированность #' + (idx + 1)"
      >
        <LabelValue :label="'Действия'" :no-print="true">
          <a 
            href="#" 
            @click="emit('delete', item['id'].toString(), 'affilation')" 
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            @click="
              affilation.action = 'update';
              affilation.item = item;
              affilation.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </LabelValue>
        <LabelValue :label="'ID'">{{ item['id'] }}</LabelValue>
        <LabelValue :label="'Тип участия'">{{ item['view'] }}</LabelValue>
        <LabelValue :label="'Организация'">{{ item['name'] }}</LabelValue>
        <LabelValue :label="'ИНН'">{{ item['inn'] }}</LabelValue>
        <LabelValue :label="'Должность'">{{ item['position'] }}</LabelValue>
        <LabelValue :label="'Дата декларации'">
          {{ new Date(String(item['deadline'])).toLocaleDateString('ru-RU') }}
        </LabelValue>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
