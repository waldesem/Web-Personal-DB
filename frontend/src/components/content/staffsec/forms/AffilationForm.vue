<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Affilation } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/InputLabel.vue")
);
const SelectArray = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/SelectArray.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/BtnGroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {},
  },
});

const affilationForm = computed(() => {
  return props.affils as Affilation;
});

const selected_item = [
  "Являлся государственным/муниципальным служащим",
  "Являлся государственным должностным лицом",
  "Связанные лица работают в государственных организациях",
  "Участвует в деятельности коммерческих организаций",
];
</script>

<template>
  <form
    @submit.prevent="emit('submit', affilationForm)"
    class="form form-check"
    role="form"
  >
    <SelectArray
      :name="'view'"
      :label="'Тип участия'"
      :select="selected_item"
      v-model="affilationForm['view']"
    />
    <InputLabel
      :name="'name'"
      :label="'Организация'"
      :need="true"
      v-model="affilationForm['name']"
    />
    <InputLabel
      :name="'inn'"
      :label="'ИНН'"
      :need="true"
      v-model="affilationForm['inn']"
    />
    <InputLabel
      :name="'position'"
      :label="'Должность'"
      :need="true"
      v-model="affilationForm['position']"
    />
    <BtnGroup>
      <BtnGroupContent/>
    </BtnGroup>
  </form>
</template>
