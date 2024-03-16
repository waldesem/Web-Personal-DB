<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Work } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/WorkplaceForm.vue")
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
        <LabelSlot>
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
        <LabelValue :label="'Начало работы'" :value="item['start_date']" />
        <LabelValue :label="'Окончание работы'" :value="item['end_date']" />
        <LabelValue :label="'Организация'" :value="item['workplace']" />
        <LabelValue :label="'КоАдреснтакт'" :value="item['address']" />
        <LabelValue :label="'Должность'" :value="item['position']" />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
