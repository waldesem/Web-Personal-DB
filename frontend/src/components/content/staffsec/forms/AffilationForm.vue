<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Affilation } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {},
  },
});

const affilationForm = computed(() => {
  return props.affils as Affilation;
});

const selected_item = {
  state: "Являлся государственным/муниципальным служащим",
  official: "Являлся государственным должностным лицом",
  relatives: "Связанные лица работают в государственных организациях",
  commercial: "Участвует в деятельности коммерческих организаций",
};
</script>

<template>
  <form
    @submit.prevent="emit('submit', affilationForm)"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'view'"
      :label="'Тип участия'"
      :select="selected_item"
      v-model="affilationForm['view']"
    />
    <InputLabel
      :name="'name'"
      :label="'Организация'"
      :need="true"
      v-model="affilationForm['name']"
    />
    <InputLabel
      :name="'inn'"
      :label="'ИНН'"
      :need="true"
      v-model="affilationForm['inn']"
    />
    <InputLabel
      :name="'position'"
      :label="'Должность'"
      :need="true"
      v-model="affilationForm['position']"
    />
    <BtnGroup :cls="false">
      <button
        class="btn btn-outline-primary btn-md"
        data-bs-dismiss="modal"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      <button 
        class="btn btn-outline-secondary btn-md" 
        name="reset" 
        type="reset"
      >
        Очистить
      </button>
    </BtnGroup>
  </form>
</template>
