<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Previous } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  previous: {
    type: Object as () => Previous,
    default: <Previous>({}),
  },
});

const anketaState = stateAnketa();

const previousForm = toRef(props.previous as Previous);

function submitPrevious() {
  anketaState.updateItem("previous", previousForm.value)
  emit('cancel');
  Object.keys(previousForm.value).forEach(
    (key) => delete previousForm.value[key as keyof typeof previousForm.value]
  );
}
</script>

<template>
  <UForm :state="previousForm" @submit.prevent="submitPrevious">
    <UFormGroup class="mb-3" label="Фамилия" required>
      <UInput
        v-model="previousForm['surname']"
        placeholder="Фамилия"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя" required>
      <UInput
        v-model="previousForm['firstname']"
        placeholder="Имя"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество">
      <UInput
        v-model="previousForm['patronymic']"
        placeholder="Отчество"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Год изменения">
      <UInput
        v-model="previousForm['changed']"
        placeholder="Год изменения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Причина изменения">
      <UInput
        v-model="previousForm['reason']"
        placeholder="Причина изменения"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
