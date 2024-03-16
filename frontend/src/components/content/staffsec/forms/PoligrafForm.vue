<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
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

const poligrafForm = computed(() => {
  return props.poligraf as Pfo;
});

const selected_item = {
  candidate: "Проверка кандидата",
  check: "Служебная проверка",
  investigation: "Служебное расследование",
};
</script>

<template>
  <form
    @submit.prevent="emit('submit', poligrafForm)"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'theme'"
      :label="'Тема проверки'"
      :select="selected_item"
      v-model="poligrafForm['theme']"
    />
    <TextLabel
      :name="'results'"
      :label="'Результат'"
      v-model="props.poligraf['results']"
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
