<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Document } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const DocumentForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/DocumentForm.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item", "document");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Document>,
    default: {},
  },
});

const document = ref({
  action: "",
  itemId: "",
  item: <Document>{},
});

const docObjs = computed(() => {
  return props.items.map((item) => ({
    id: ["ID", item['id']],
    view: ["Вид документа", item['view']],
    number: ["Номер документа", item['number']],
    series: ["Серия документа", item['series']],
    issuer: ["Кем выдан", item['agency']],
    date: ["Дата выдачи", new Date(String(item['issue'])).toLocaleDateString('ru-RU')],
  }));
});

function submitForm(form: Object) {
  emit("submit", document.value.action, "document", document.value.itemId, form)
  document.value.action = '';
};
</script>

<template>
   <h6>
    Документы
    <a
      class="btn btn-link"
      @click="
        document.action = document.action ? '' : 'create';"
      title="Добавить информацию"
    >
      <i class="bi bi-plus-circle"></i>
    </a>
  </h6>
  <DocumentForm v-if="document.action"
    :docs="document.item"
    @submit="submitForm"
  />
  <div v-else>
    <div v-if="docObjs.length">
      <CollapseDiv
        v-for="(item, idx) in docObjs"
        :key="idx"
        :id="'docum' + idx"
        :idx="idx.toString()"
        :label="'Документ #' + (idx + 1)"
      >
      <div class="row mb-3 d-print-none">
        <div class="col-md-3">
          <label class="form-label">Действия</label>
        </div>
        <div class="col-md-9">
          <a
            href="#"
            @click="
              emit('delete', item.id[1].toString(), 'document')"
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            @click="
              document.action = 'update';
              document.item = props.items[idx];
              document.itemId = item.id[1].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </div>
      </div>
      <div v-for="value, key in item" :key="key" class="row mb-3">
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
