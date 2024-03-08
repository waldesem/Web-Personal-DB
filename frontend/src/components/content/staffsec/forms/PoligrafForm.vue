<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Pfo } from "@/interfaces/interface";

const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: {},
  },
});

const poligrafForm = ref({
  form: <Pfo>{},
  selected_item: {
    candidate: "Проверка кандидата",
    check: "Служебная проверка",
    investigation: "Служебное расследование",
  }
});

function updateItem() {
  emit("submit", poligrafForm.value.form);
  Object.keys(poligrafForm.value.form).forEach((key) => {
    delete poligrafForm.value.form[key as keyof typeof poligrafForm.value.form];
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
      :name="'theme'"
      :label="'Тема проверки'"
      :select="poligrafForm.selected_item"
      :model="props.poligraf['theme']"
      @input-event="
        poligrafForm.form['theme'] = $event.target.value
      "
    />
    <TextLabel
      :name="'results'"
      :label="'Результат'"
      :model="props.poligraf['results']"
      @input-event="
        poligrafForm.form['results'] = $event.target.value
      "
    />
    <BtnGroup>
      <button
        class="btn btn-outline-primary btn-md"
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
