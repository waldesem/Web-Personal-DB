<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Document } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const DocumentForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/DocumentForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
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
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'docum' + idx"
        :idx="idx.toString()"
        :label="'Документ #' + (idx + 1)"
      >
        <LabelValue :label="'Действия'" :no-print="true">
          <a
            href="#"
            @click="
              emit('delete', item['id'].toString(), 'document')"
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
        </LabelValue>
        <LabelValue :label="'ID'">{{ item['id'] }}</LabelValue>
        <LabelValue :label="'Вид документа'">{{ item['view'] }}</LabelValue>
        <LabelValue :label="'Номер документа'">{{ item['number'] }}</LabelValue>
        <LabelValue :label="'Серия документа'">{{ item['series'] }}</LabelValue>
        <LabelValue :label="'Кем выдан'">{{ item['agency'] }}</LabelValue>
        <LabelValue :label="'Дата выдачи'">
          {{ new Date(String(item['issue'])).toLocaleDateString('ru-RU') }}
        </LabelValue>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
