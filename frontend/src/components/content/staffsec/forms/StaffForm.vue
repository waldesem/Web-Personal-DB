<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Staff } from "@/interfaces/interface";

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
  staff: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const staffForm = ref({
  form: <Staff>{},

  submitForm: function () {
    emit("submit", this.form);
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
   },
});
</script>

<template>
  <form
    @submit.prevent="staffForm.submitForm;"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'position'"
      :label="'Должность'"
      :need="true"
      :model="props.staff['position']"
      @input-event="staffForm.form['position'] = $event.target.value"
    />
    <TextLabel
      :name="'department'"
      :label="'Подраздление'"
      :model="props.staff['department']"
      @input-event="staffForm.form['department'] = $event.target.value"
    />
    <BtnGroup :cls="false">
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
    </BtnGroup>
  </form>
</template>
