<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Document } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const DocumentForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/DocumentForm.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
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

function cancelEdit(){
  document.value.action = '';
  document.value.item = <Document>{};
};

function submitForm(form: Object) {
  emit("submit", document.value.action, "document", document.value.itemId, form)
};

function deleteItem(itemId: string){
  emit("delete", itemId, "document")
};
</script>

<template>
   <h6>
    Документы
    <a
      class="btn btn-link"
      data-bs-toggle="modal"
      data-bs-target="#modalDoc"
      @click="
        document.action = document.action ? '' : 'create';"
      title="Добавить информацию"
    >
      <i class="bi bi-plus-circle"></i>
    </a>
  </h6>
  <ModalWin
    :title="
      document.action === 'update' ? 'Изменить запись' : 'Добавить запись'
    "
    :id="'modalDoc'"
    @cancel="cancelEdit"
  >
    <DocumentForm 
      :content="document.item"
      @submit="submitForm"
    />
  </ModalWin>
  <div v-if="props.items.length > 0">
    <CollapseDiv
      v-for="(item, idx) in props.items"
      :key="idx"
      :id="'docum' + idx"
      :idx="idx.toString()"
      :label="'Документ #' + (idx + 1)"
    >
    <LabelSlot>
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
        data-bs-toggle="modal"
        data-bs-target="#modalDoc"
        @click="
          document.action = 'update';
          document.item = item;
          document.itemId = item['id'].toString();
        "
      >
        <i class="bi bi-pencil-square"></i>
      </a>
    </LabelSlot>
    <LabelValue :label="'Вид документа'" :value="item['view']" />
    <LabelValue :label="'Серия'" :value="item['series']" />
    <LabelValue :label="'Номер'" :value="item['number']" />
    <LabelValue :label="'Кем выдан'" :value="item['agency']" />
    <LabelValue
      :label="'Дата выдачи'"
      :value="new Date(String(item['issue'])).toLocaleDateString('ru-RU')"
    />
    </CollapseDiv>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
