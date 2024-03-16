<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
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

const relationForm = computed(() => {
  return props.relation as Relation;
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', relationForm)"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'relation'"
      :label="'Тип связи'"
      :need="true"
      v-model="relationForm['relation']"
    />
    <InputLabel
      :name="'relation_id'"
      :label="'ID связи'"
      :need="true"
      v-model="relationForm['relation_id']"
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
