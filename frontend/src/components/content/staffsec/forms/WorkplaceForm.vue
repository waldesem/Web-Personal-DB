<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Work } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  work: {
    type: Object as () => Work,
    default: {},
  },
});

const workForm = ref({
  form: <Work>{},
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', workForm.form)"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'start_date'"
      :label="'Начало работы'"
      :typeof="'date'"
      :model="props.work['start_date']"
      @input-event="
        workForm.form['start_date'] = $event.target.value
      "
    />
    <InputLabel
      :name="'end_date'"
      :label="'Окончание работы'"
      :typeof="'date'"
      :model="props.work['end_date']"
      @input-event="
        workForm.form['end_date'] = $event.target.value
      "
    />
    <InputLabel
      :name="'workplace'"
      :label="'Место работы'"
      :need="true"
      :model="props.work['workplace']"
      @input-event="
        workForm.form['workplace'] = $event.target.value
      "
    />
    <TextLabel
      :name="'address'"
      :label="'Адрес организации'"
      :model="props.work['address']"
      @input-event="
        workForm.form['address'] = $event.target.value
      "
    />
    <TextLabel
      :name="'position'"
      :label="'Должность'"
      :model="props.work['position']"
      @input-event="
        workForm.form['position'] = $event.target.value
      "
    />
    <TextLabel
      :name="'reason'"
      :label="'Причина увольнения'"
      :model="props.work['reason']"
      @input-event="
        workForm.form['reason'] = $event.target.value
      "
    />
    <BtnGroup>
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
