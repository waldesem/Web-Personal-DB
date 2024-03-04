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

const emit = defineEmits(["get", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get", "workplace");
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

const workplace = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Record<any, string>>{},
});

function deactivateEmit() {
  workplace.value.isForm = false; 
  workplace.value.action = '';
};

function submitForm(
  itemId: string, 
  form: Object
  ) {
  emit("submit", [workplace.value.action, "workplace", itemId, form])
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
      @click="
        workplace.isForm = !workplace.isForm;  
        workplace.action = 'create'"
      :title="workplace.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="workplace.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="workplace.isForm">
    <WorkplaceForm 
      :action="workplace.action"
      :cand-id="candId"
      :content="workplace.item"
      @submit="submitForm"
      @deactivate="deactivateEmit"
    />
  </template>
  <template v-else>
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
              @click="
                workplace.isForm = true;
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
  
</template>
