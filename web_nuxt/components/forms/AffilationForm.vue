<script setup lang="ts">
import type { Affilation } from "@/types/interfaces";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {} as Affilation,
  },
  candId: {
    type: String,
    default: "",
  },
});

const affilationForm = toRef(props.affils as Affilation);

function submitAffilation() {
  emit("update", affilationForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(affilationForm.value, {
    view: "",
    organization: "",
    inn: "",
  } as Affilation);
}
</script>

<template>
  <UForm :state="affilationForm" @submit.prevent="submitAffilation">
    <UFormGroup class="mb-3" label="Тип участия">
      <USelect
        v-model.trim.lazy="affilationForm['view']"
        required
        :options="[
          'Являлся государственным/муниципальным служащим',
          'Являлся государственным должностным лицом',
          'Связанные лица работают в государственных организациях',
          'Участвует в деятельности коммерческих организаций',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Организация">
      <UInput
        v-model.trim.lazy="affilationForm['organization']"
        required
        placeholder="Организация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН">
      <UInput v-model.trim.lazy="affilationForm['inn']" placeholder="ИНН" />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
