<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const StaffForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/StaffForm.vue")
);

const emit = defineEmits(["get", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get", "staff");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Array<Record<string, any>>,
    default: () => {},
  },
});

const staff = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Record<string, any>>{},
});

function deactivateEmit() {
  staff.value.isForm = false; 
  staff.value.action = '';
};

function submitForm(
  itemId: string, 
  form: Object
  ) {
  emit("submit", [staff.value.action, "staff", itemId, form])
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "staff"])
};
</script>

<template>
  <h6>
    Должности
    <a
      class="btn btn-link"
      @click="
        staff.isForm = !staff.isForm;
        staff.action = staff.isForm ? 'create' : '';"
      :title="staff.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="staff.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="staff.isForm">
    <StaffForm
      :action="staff.action"
      :cand-id="candId"
      :content="staff.item"
      @submit="submitForm"
      @deactivate="deactivateEmit"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'staff' + idx.toString()"
        :idx="idx.toString()"
        :label="'Должность #' + (idx + 1).toString()"
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
                staff.isForm = true;
                staff.action = 'update';
                staff.item = item;
                staff.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Должность'" :value="item['position']" />
        <RowDivSlot :label="'Департамент'" :value="item['department']" />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
