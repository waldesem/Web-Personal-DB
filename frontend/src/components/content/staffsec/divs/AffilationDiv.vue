<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Affilation } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/AffilationForm.vue")
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

const affilObj = computed(() => {
  return props.items.map((item) => ({
    id: ["ID", item['id']],
    view: ["Тип участия", item['view']],
    comment: ["Организация", item['name']],
    inn: ["ИНН", item['inn']],    
    position: ["Должность", item['position']],
    deadline: [
      "Дата декларации", new Date(String(item['deadline'])).toLocaleDateString('ru-RU')
    ]
  }))
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
    <div v-if="affilObj.length">
      <CollapseDiv
        v-for="(item, idx) in affilObj"
        :key="idx"
        :id="'affil' + idx"
        :idx="idx.toString()"
        :label="'Аффилированность #' + (idx + 1)"
      >
        <div class="row mb-3 d-print-none">
          <div class="col-md-3">
            <label class="form-label">Действия</label>
          </div>
          <div class="col-md-9">
            <a 
              href="#" 
              @click="emit('delete', item.id[1].toString(), 'affilation')" 
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                affilation.action = 'update';
                affilation.item = props.items[idx];
                affilation.itemId = item.id[1].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </div>
        </div>
        <div v-for="(value, key) in item" :key="key" class="row mb-3">
          <div class="col-md-3">
            <label class="form-label">
              {{ value[0] }}
            </label>
          </div>
          <div class="col-md-9">
            {{ value[1] }}
          </div>
        </div>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
