<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Document } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const DocumentForm = defineAsyncComponent(
  () => import("@components/content/forms/DocumentForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
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
        <LabelSlot :label="'Действия'" :no-print="true">
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
        </LabelSlot>
        <LabelSlot :label="'ID'">{{ item['id'] }}</LabelSlot>
        <LabelSlot :label="'Вид документа'">{{ item['view'] }}</LabelSlot>
        <LabelSlot :label="'Номер документа'">{{ item['number'] }}</LabelSlot>
        <LabelSlot :label="'Серия документа'">{{ item['series'] }}</LabelSlot>
        <LabelSlot :label="'Кем выдан'">{{ item['agency'] }}</LabelSlot>
        <LabelSlot :label="'Дата выдачи'">
          {{ new Date(String(item['issue'])).toLocaleDateString('ru-RU') }}
        </LabelSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
