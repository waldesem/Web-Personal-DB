<script setup lang="ts">
import { toRef } from "vue";
import type { Previous } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  previous: {
    type: Object as () => Previous,
    default: {} as Previous,
  },
});

const previousForm = toRef(props.previous as Previous);

function submitPrevious() {
  emit("submit", previousForm.value);
  cancelAction();
}

function cancelAction() {
  emit('cancel');
  Object.assign(previousForm.value, {
    surname: "",
    firstname: "",
    patronymic: "",
    changed: "",
    reason: "",
  } as Previous);
}
</script>

<template>
  <UForm :state="previousForm" @submit.prevent="submitPrevious">
    <UFormGroup class="mb-3" label="Фамилия">
      <UInput
        v-model.trim.lazy="previousForm['surname']"
        required
        placeholder="Фамилия"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя">
      <UInput
        v-model.trim.lazy="previousForm['firstname']"
        required
        placeholder="Имя"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество">
      <UInput
        v-model.trim.lazy="previousForm['patronymic']"
        placeholder="Отчество"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Год изменения">
      <UInput
        v-model.trim.lazy="previousForm['changed']"
        placeholder="Год изменения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Причина изменения">
      <UInput
        v-model.trim.lazy="previousForm['reason']"
        placeholder="Причина изменения"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction"/>
  </UForm>
</template>
