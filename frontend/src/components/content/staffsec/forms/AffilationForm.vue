<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Affilation } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
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

const affilationForm = ref({
  form: <Affilation>{},
  selected_item: {
    state: "Являлся государственным/муниципальным служащим",
    official: "Являлся государственным должностным лицом",
    relatives: "Связанные лица работают в государственных организациях",
    commercial: "Участвует в деятельности коммерческих организаций",
  }
});

function updateItem() {
  emit("submit", affilationForm.value.form);
  Object.keys(affilationForm.value.form).forEach((key) => {
    delete affilationForm.value.form[key as keyof typeof affilationForm.value.form];
  });
};
</script>

<template>
  <form
    @submit.prevent="updateItem"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'view'"
      :label="'Тип участия'"
      :select="affilationForm.selected_item"
      :model="props.affils['view']"
      @input-event="affilationForm.form['view'] = $event.target.value"
    />
    <TextLabel
      :name="'name'"
      :label="'Организация'"
      :model="props.affils['name']"
      @input-event="affilationForm.form['name'] = $event.target.value"
    />
    <InputLabel
      :name="'inn'"
      :label="'ИНН'"
      :need="true"
      :model="props.affils['inn']"
      @input-event="affilationForm.form['inn'] = $event.target.value"
    />
    <TextLabel
      :name="'position'"
      :label="'Должность'"
      :model="props.affils['position']"
      @input-event="
        affilationForm.form['position'] = $event.target.value
      "
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
