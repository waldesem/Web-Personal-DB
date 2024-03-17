<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Staff } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const StaffForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/StaffForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item", "staff");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Staff>,
    default: {},
  },
});

const staff = ref({
  action: "",
  itemId: "",
  item: <Staff>{},
});

function submitForm(form: Object) {
  emit("submit", staff.value.action, "staff", staff.value.itemId, form)
  staff.value.action = ""
};  
</script>

<template>
  <h6>
    Должности
    <a
      class="btn btn-link"
      @click="
        staff.action = staff.action ? '' : 'create';"
        :title="'Добавить информацию'"
    >
      <i
        :class="staff.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <StaffForm v-if="staff.action"
    :staff="staff.item"
    @submit="submitForm"
  />
  <div v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'staff' + idx"
        :idx="idx.toString()"
        :label="'Должность #' + (idx + 1)"
      >
        <div class="row mb-3 d-print-none">
          <div class="col-md-3">
            <label class="form-label">Действия</label>
          </div>
          <div class="col-md-9">
            <a
              href="#"
              @click="emit('delete', item['id'].toString(), 'staff')"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
                @click="
                staff.action = 'update';
                staff.item = item;
                staff.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </div>
        </div>
        <LabelValue
         :label="'ID'"
         :value="item['id']"
        />
        <LabelValue
         :label="'Должность'"
         :value="item['position']"
        />
        <LabelValue
         :label="'Департамент'"
         :value="item['department']"
        />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
