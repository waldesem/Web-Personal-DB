<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const DocumentForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/DocumentForm.vue")
);

const emit = defineEmits(["get", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get", "document");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const document = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Record<any, string>>{},
});

function deactivateEmit() {
  document.value.isForm = false; 
  document.value.action = '';
};

function submitForm(
  itemId: string, 
  form: Object
  ) {
  emit("submit", [document.value.action, "document", itemId, form])
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "document"])
};
</script>

<template>
   <h6>
    Документы
    <a
      class="btn btn-link"
      @click="
        document.isForm = !document.isForm;
        document.action = document.isForm ? 'create' : '';"
      :title="document.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="document.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="document.isForm">
    <DocumentForm 
      :action="document.action"
      :cand-id="candId"
      :content="document.item"
      @submit="submitForm"
      @deactivate="deactivateEmit"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'docum' + idx.toString()"
        :idx="idx.toString()"
        :label="'Документ #' + (idx + 1).toString()"
      >
      <RowDivSlot :slotTwo="true" :print="true">
        <template v-slot:divTwo>
          <a
            href="#"
            @click="
              deleteItem(item['id'].toString())"
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            @click="
              document.isForm = true;
              document.action = 'update';
              document.item = item;
              document.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </template>
      </RowDivSlot>
      <RowDivSlot :label="'Вид документа'" :value="item['view']" />
      <RowDivSlot :label="'Серия'" :value="item['series']" />
      <RowDivSlot :label="'Номер'" :value="item['number']" />
      <RowDivSlot :label="'Кем выдан'" :value="item['agency']" />
      <RowDivSlot
        :label="'Дата выдачи'"
        :value="new Date(String(item['issue'])).toLocaleDateString('ru-RU')"
      />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
