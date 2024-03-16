<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Document } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
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
      <LabelSlot>
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
  </div>
</template>
