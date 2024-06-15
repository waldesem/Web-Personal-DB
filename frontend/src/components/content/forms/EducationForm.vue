<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Education } from "@/interfaces";
import { clearForm } from "@/utilities";
import { stateClassify } from "@/state";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
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
</script>

<template>
  <form
    @submit.prevent="emit('submit', educationForm); clearForm(educationForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Вид образования'">
      <SelectDiv
        :name="'type'"
        :select="stateClassify.educations"
        v-model="educationForm['view']"
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
        :name="'finish'"
        :place="'Год окончания'"
        :need="true"
        v-model="educationForm['finished']"
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
