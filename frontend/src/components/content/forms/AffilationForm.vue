<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Affilation } from "@/interfaces/interface";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectInput = defineAsyncComponent(
  () => import("@components/content/elements/SelectInput.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
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
    <LabelSlot :label="'Тип участия'">
      <SelectInput
        :name="'view'"
        :select="selected_item"
        v-model="affilationForm['view']"
      />
    </LabelSlot>
    <InputElement
      :name="'name'"
      :label="'Организация'"
      :need="true"
      v-model="affilationForm['name']"
    />
    <InputElement
      :name="'inn'"
      :label="'ИНН'"
      :need="true"
      v-model="affilationForm['inn']"
    />
    <InputElement
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
