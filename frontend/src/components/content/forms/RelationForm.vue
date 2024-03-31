<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Relation } from "@/interfaces/interface";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroupContent.vue")
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
    <InputElement
      :name="'relation'"
      :label="'Тип связи'"
      :need="true"
      v-model="relationForm['relation']"
    />
    <InputElement
      :name="'relation_id'"
      :label="'ID связи'"
      :need="true"
      v-model="relationForm['relation_id']"
    />
    <BtnGroup>
      <BtnGroupContent/>
    </BtnGroup>
  </form>
</template>
