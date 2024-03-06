<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/WorkplaceForm.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get-item", "workplace");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const workplace = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
});

function cancelEdit(){
  workplace.value.action = '';
  workplace.value.item = {};
};

function submitForm(form: Object) {
  emit("submit", [workplace.value.action, "workplace", workplace.value.itemId, form])
  cancelEdit();
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "workplace"])
};
</script>

<template>
  <h6>
    Работа
    <a
      class="btn btn-link"
      data-bs-toggle="modal"
      data-bs-target="#modalWork"
      @click="
        workplace.action = workplace.action ? '' : 'create';"
        :title="workplace.action ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="workplace.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <ModalWin
    :title="
      workplace.action === 'update' ? 'Изменить запись' : 'Добавить запись'
    "
    :id="'modalAddress'"
    @cancel="cancelEdit"
  >
    <WorkplaceForm 
      :content="workplace.item"
      @submit="submitForm"
      @cancel="cancelEdit"
    />
  </ModalWin>
  <div v-if="props.items.length > 0">
    <CollapseDiv
      v-for="(item, idx) in props.items"
      :key="idx"
      :id="'work' + idx.toString()"
      :idx="idx.toString()"
      :label="'Работа #' + (idx + 1).toString()"
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
            data-bs-toggle="modal"
            data-bs-target="#modalWork"
            @click="
              workplace.action = 'update';
              workplace.item = item;
              workplace.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </template>
      </RowDivSlot>
      <RowDivSlot :label="'Начало работы'" :value="item['start_date']" />
      <RowDivSlot :label="'Окончание работы'" :value="item['end_date']" />
      <RowDivSlot :label="'Организация'" :value="item['workplace']" />
      <RowDivSlot :label="'КоАдреснтакт'" :value="item['address']" />
      <RowDivSlot :label="'Должность'" :value="item['position']" />
    </CollapseDiv>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
