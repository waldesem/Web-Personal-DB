<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Work } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/content/forms/WorkplaceForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
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
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'work' + idx"
        :idx="idx.toString()"
        :label="'Работа #' + (idx + 1)"
      >
        <LabelSlot :label="'Действия'" :no-print="true">
          <a href="#" 
            @click="emit('delete', item['id'].toString(), 'workplace')" 
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            @click="
              workplace.action = 'update';
              workplace.item = item;
              workplace.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </LabelSlot>
        <LabelSlot :label="'ID'">{{ item['id'] }}</LabelSlot>
        <LabelSlot :label="'Начало работы'">{{ item['start_date'] }}</LabelSlot>
        <LabelSlot :label="'Окончание работы'">{{ item['end_date'] }}</LabelSlot>
        <LabelSlot :label="'Место работы'">{{ item['workplace'] }}</LabelSlot>
        <LabelSlot :label="'Адрес'">{{ item['address'] }}</LabelSlot>
        <LabelSlot :label="'Должность'">{{ item['position'] }}</LabelSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
