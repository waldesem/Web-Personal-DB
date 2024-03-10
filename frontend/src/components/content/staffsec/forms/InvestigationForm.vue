<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces/interface";

const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: {},
  },
});

const investigationForm = ref({
  form: <Inquisition>{},
  });
</script>

<template>
  <form
    @submit.prevent="emit('submit', investigationForm.form)"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'theme'"
      :label="'Тема проверки'"
      :need="true"
      :model="props.investigation['theme']"
      @input-event="
        investigationForm.form['theme'] = $event.target.value
      "
    />
    <TextLabel
      :name="'info'"
      :label="'Информация'"
      :model="props.investigation['info']"
      @input-event="investigationForm.form['info'] = $event.target.value"
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
