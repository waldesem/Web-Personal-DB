<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Relation } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {},
  },
});

const relationForm = ref({
  form: <Relation>{},
  });

function updateItem() {
  emit("submit", relationForm.value.form);
  Object.keys(relationForm.value.form).forEach((key) => {
    delete relationForm.value.form[key as keyof typeof relationForm.value.form];
  });
};
</script>

<template>
  <form
    @submit.prevent="updateItem"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'relation'"
      :label="'Тип связи'"
      :need="true"
      :model="props.relation['relation']"
      @input-event="
        relationForm.form['relation'] = $event.target.value
      "
    />
    <InputLabel
      :name="'relation_id'"
      :label="'ID связи'"
      :need="true"
      :model="props.relation['relation_id']"
      @input-event="
        relationForm.form['relation_id'] = $event.target.value
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
