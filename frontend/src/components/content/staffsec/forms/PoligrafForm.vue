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

const emit = defineEmits(["submit", "cancel"]);

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
</script>

<template>
  <form
    @submit.prevent="emit('submit', poligrafForm.form)"
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
      <button
        class="btn btn-outline-danger btn-md"
        type="button"
        @click="emit('cancel')"
        name="cancel"
      >
      Отмена
      </button>
    </BtnGroup>
  </form>
</template>
