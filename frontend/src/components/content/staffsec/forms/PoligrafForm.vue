<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Pfo } from "@/interfaces/interface";

const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const poligrafForm = ref({
  form: <Pfo>{},
  selected_item: {
    candidate: "Проверка кандидата",
    check: "Служебная проверка",
    investigation: "Служебное расследование",
  },

  updateItem: function () {
    emit("submit", this.form);
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
   },
});
</script>

<template>
  <form
    @submit.prevent="poligrafForm.updateItem"
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
    <BtnGroupForm :cls="false">
      <button
        class="btn btn-outline-success btn-md"
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
    </BtnGroupForm>
  </form>
</template>
