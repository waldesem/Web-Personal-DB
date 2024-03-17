<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Work } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/WorkplaceForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(async () => {
  emit("get-item", "workplace");
});

const props = defineProps({
  items: {
    type: Array as () => Array<Work>,
    default: {},
  },
});

const workplace = ref({
  action: "",
  itemId: "",
  item: <Work>{},
});

const workObjects = computed(() => {
  return props.items.map((item) => ({
    id: ["ID", item["id"]],
    start_date: ["Начало работы", item["start_date"]],
    end_date: ["Окончание работы", item["end_date"]],
    workplace: ["Место работы", item["workplace"]],
    address: ["Адрес", item["address"]],
    position: ["Должность", item["position"]],
  }));
});
    
function submitForm(form: Object) {
  emit(
    "submit", 
    workplace.value.action,
    "workplace",
    workplace.value.itemId,
    form,
  );
  workplace.value.action = "";
};
</script>

<template>
  <h6>
    Работа
    <a
      class="btn btn-link"
      @click="workplace.action = workplace.action ? '' : 'create'"
      :title="workplace.action ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="workplace.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      >
      </i>
    </a>
  </h6>
  <WorkplaceForm v-if="workplace.action"
    :content="workplace.item"
    @submit="submitForm"
  />
  <div v-else>
    <div v-if="workObjects.length">
      <CollapseDiv
        v-for="(item, idx) in workObjects"
        :key="idx"
        :id="'work' + idx"
        :idx="idx.toString()"
        :label="'Работа #' + (idx + 1)"
      >
        <div class="row mb-3 d-print-none">
          <div class="col-md-3">
            <label class="form-label">Действия</label>
          </div>
          <div class="col-md-9">
            <a href="#" 
              @click="emit('delete', item.id[1].toString(), 'workplace')" 
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                workplace.action = 'update';
                workplace.item = props.items[idx];
                workplace.itemId = item.id[1].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </div>
        </div>
        <LabelValue v-for="(value, key) in item" :key="key"
          :label="value[0]"
          :value="value[1]"
        />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
