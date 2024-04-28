<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Education } from "@/interfaces";
import { clearForm } from "@/utilities";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectArray = defineAsyncComponent(
  () => import("@components/content/elements/SelectArray.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  docs: {
    type: Object as () => Education,
    default: {},
  },
});

const educationForm = toRef(props.docs as Education);

const selected_item = [
  "Среднее",
  "Среднее специальное",
  "Высшее",
  "Неоконченное высшее",
  "Другое",
];
</script>

<template>
  <form
    @submit.prevent="emit('submit', educationForm); clearForm(educationForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Вид образования'">
      <SelectArray
        :name="'type'"
        :select="selected_item"
        v-model="educationForm['type']"
      />
    </LabelSlot>
    <LabelSlot :label="'Название учебного заведения'">
      <InputElement
        :name="'name'"
        :place="'Название учебного заведения'"
        v-model="educationForm['name']"
      />
    </LabelSlot>
    <LabelSlot :label="'Год окончания'">
      <InputElement
        :name="'end'"
        :place="'Год окончания'"
        :need="true"
        v-model="educationForm['end']"
      />
    </LabelSlot>
    <LabelSlot :label="'Специальность'">
      <InputElement
        :name="'speciality'"
        :place="'Специальность'"
        v-model="educationForm['speciality']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
