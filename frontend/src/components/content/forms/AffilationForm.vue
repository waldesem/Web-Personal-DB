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
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

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
    <LabelSlot :label="'Организация'">
      <InputElement
        :name="'name'"
        :place="'Организация'"
        :need="true"
        v-model="affilationForm['name']"
      />
    </LabelSlot>
    <LabelSlot :label="'ИНН'">
      <InputElement
        :name="'inn'"
        :place="'ИНН'"
        :need="true"
        v-model="affilationForm['inn']"
      />
    </LabelSlot>
    <LabelSlot :label="'Должность'">
      <InputElement
        :name="'position'"
        :place="'Должность'"
        :need="true"
        v-model="affilationForm['position']"
      />
    </LabelSlot>
    <BtnGroup>
      <GroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
