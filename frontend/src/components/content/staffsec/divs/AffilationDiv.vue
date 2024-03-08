<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Affilation } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/AffilationForm.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
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

function cancelEdit() {
  affilation.value.action = "";
  affilation.value.item = <Affilation>{};
}

function submitForm(form: Object) {
  emit("submit", [
    affilation.value.action,
    "affilation",
    affilation.value.itemId,
    form,
  ]);
  cancelEdit();
}

function deleteItem(itemId: string) {
  emit("delete", [itemId, "affilation"]);
}
</script>

<template>
  <h6>
    Аффилированность
    <a
      class="btn btn-link"
      @click="affilation.action = affilation.action ? '' : 'create'"
      data-bs-toggle="modal"
      data-bs-target="#modalAffilation"
      title="Добавить информацию"
    >
      <i class="bi bi-plus-circle"></i>
    </a>
  </h6>
  <ModalWin
    :title="
      affilation.action === 'update' ? 'Изменить адрес' : 'Добавить организацию'
    "
    :id="'modalAffilation'"
    @cancel="cancelEdit"
  >
    <AffilationForm :content="affilation.item" @submit="submitForm" />
  </ModalWin>
  <div v-if="props.items.length > 0">
    <CollapseDiv
      v-for="(item, idx) in props.items"
      :key="idx"
      :id="'affil' + idx"
      :idx="idx.toString()"
      :label="'Аффилированность #' + (idx + 1)"
    >
      <LabelSlot>
        <a href="#" @click="deleteItem(item['id'].toString())" title="Удалить">
          <i class="bi bi-trash"></i>
        </a>
        <a
          class="btn btn-link"
          title="Изменить"
          data-bs-toggle="modal"
          data-bs-target="#modalAffilation"
          @click="
            affilation.action = 'update';
            affilation.item = item;
            affilation.itemId = item['id'].toString();
          "
        >
          <i class="bi bi-pencil-square"></i>
        </a>
      </LabelSlot>
      <LabelValue :label="'Тип участия'" :value="item['view']" />
      <LabelValue :label="'Организация'" :value="item['name']" />
      <LabelValue :label="'ИНН'" :value="item['inn']" />
      <LabelValue :label="'Должность'" :value="item['position']" />
      <LabelValue
        :label="'Дата декларации'"
        :value="new Date(item['deadline']).toLocaleDateString('ru-RU')"
      />
    </CollapseDiv>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
