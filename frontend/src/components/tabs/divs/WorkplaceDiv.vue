<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Work } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/forms/WorkplaceForm.vue")
);


onBeforeMount( async() => {
  await props.getItem("staff");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Work[],
    default: () => ({}),
  },
  getItem: {
    type: Function,
    required: true,
  },
  deleteItem: {
    type: Function,
    required: true,
  },
});

const workplace = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Work>{},

  deactivateForm: function () {
    this.isForm = false;
    this.action = "";
  },
});
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
      :get-item="props.getItem"
      :action="workplace.action"
      :cand-id="candId"
      :content="workplace.item"
      @deactivate="workplace.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'work' + idx"
        :idx="idx"
        :label="'Работа #' + (idx + 1)"
      >
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="props.deleteItem(item['id'].toString())"
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
