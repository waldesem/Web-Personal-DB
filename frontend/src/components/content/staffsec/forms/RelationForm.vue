<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Relation } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  relation: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const relationForm = ref({
  form: <Relation>{},

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
    @submit.prevent="relationForm.updateItem"
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
      <button 
        class="btn btn-outline-primary btn-md" 
        name="cancel" 
        type="button"
        @click="$emit('cancel')"
      >
        Отмена
      </button>
    </BtnGroupForm>
  </form>
</template>
