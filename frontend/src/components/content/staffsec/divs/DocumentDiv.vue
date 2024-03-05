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

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get-item", "document");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const document = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
});

function cancelEdit(){
  document.value.action = '';
  document.value.item = {};
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
        document.action = document.action ? '' : 'create';"
        :title="document.action ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="document.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="document.action">
    <DocumentForm 
      :content="document.item"
      @submit="submitForm"
      @deactivate="cancelEdit"
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
