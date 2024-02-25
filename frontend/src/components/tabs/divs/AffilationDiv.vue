<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Affilation } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/forms/AffilationForm.vue")
);


onBeforeMount( async() => {
  await props.getItem("staff");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Affilation[],
    default: () => ({}),
  },
  getItem: {
    type: Function,
    required: true,
  },
  updateItem: {
    type: Function,
    required: true,
  },
  deleteItem: {
    type: Function,
    required: true,
  },
});

const affilation = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Affilation>{},
});
</script>

<template>
  <h6>
    Аффилированность
    <a
      class="btn btn-link"
      @click="
        affilation.isForm = !affilation.isForm;
        affilation.action = affilation.isForm ? 'create' : '';"
      :title="affilation.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="affilation.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="affilation.isForm">
    <AffilationForm 
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :action="affilation.action"
      :cand-id="candId"
      :content="affilation.item"
      @deactivate="affilation.isForm = false; affilation.action = '';"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'affil' + idx"
        :idx="idx"
        :label="'Аффилированность #' + (idx + 1)"
      >
      <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="props.deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                affilation.isForm = true;
                affilation.action = 'update';
                affilation.item = item;
                affilation.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Тип участия'" :value="item['view']" />
        <RowDivSlot :label="'Организация'" :value="item['name']" />
        <RowDivSlot :label="'ИНН'" :value="item['inn']" />
        <RowDivSlot :label="'Должность'" :value="item['position']" />
        <RowDivSlot
          :label="'Дата декларации'"
          :value="new Date(item['deadline']).toLocaleDateString('ru-RU')"
        />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
