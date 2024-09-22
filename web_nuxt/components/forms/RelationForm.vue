<script setup lang="ts">
import type { Relation } from "@/types/interfaces";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {} as Relation,
  },
  candId: {
    type: String,
    default: "",
  },
});

const relationForm = toRef(props.relation as Relation);

async function submitRelation() {
  emit("update", relationForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(relationForm.value, {
    relation: "",
    relation_id: "",
  } as Relation);
}
</script>

<template>
  <UForm :state="relationForm" @submit.prevent="submitRelation">
    <UFormGroup class="mb-3" label="Тип связи">
      <USelect
        v-model.trim.lazy="relationForm['relation']"
        required
        :options="[
          'Одно лицо',
          'Родители-Дети',
          'Братья-Сестры',
          'Супруг-Супруга',
          'Родственники',
          'Близкая связь',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ID связи">
      <UInput
        v-model.trim.lazy="relationForm['relation_id']"
        required
        type="number"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
