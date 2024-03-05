<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/AffilationForm.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get-item", "affilation");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const affilation = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
});

function cancelEdit() {
  affilation.value.action = '';
  affilation.value.item = {};
};

function submitForm(
  itemId: string, 
  form: Object
  ) {
  emit("submit", [affilation.value.action, "affilation", itemId, form])
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "affilation"])
};
</script>

<template>
  <h6>
    Аффилированность
    <a
      class="btn btn-link"
      @click="
        affilation.action = affilation.action ? '' : 'create';"
        :title="affilation.action ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="affilation.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="affilation.action">
    <AffilationForm 
      :content="affilation.item"
      @submit="submitForm"
      @cancel="cancelEdit"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'affil' + idx.toString()"
        :idx="idx.toString()"
        :label="'Аффилированность #' + (idx + 1).toString()"
      >
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="deleteItem(item['id'].toString())"
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
