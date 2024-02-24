<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Staff } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const StaffForm = defineAsyncComponent(
  () => import("@components/forms/StaffForm.vue")
);

onBeforeMount(() => {
  props.getItem("staff");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Staff[],
    default: () => {},
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

const staff = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Staff>{},

  deactivateForm: function () {
    this.isForm = false;
    this.action = "";
  },
});
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
      :get-item="props.getItem"
      :action="staff.action"
      :cand-id="candId"
      :content="staff.item"
      @deactivate="staff.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'staff' + idx"
        :idx="idx"
        :label="'Должность #' + (idx + 1)"
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
