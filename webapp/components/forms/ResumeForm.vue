<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Persons } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  action: {
    type: String,
    default: "create",
  },
  resume: {
    type: Object as () => Persons,
    default: <Persons>({}),
  },
});

const anketaState = stateAnketa();

const resumeForm = toRef(props.resume);

function cancelEdit() {
  Object.keys(resumeForm.value).forEach(
    (key) => delete resumeForm.value[key as keyof typeof resumeForm.value]
  );
  emit('cancel')
}

async function submitForm(): Promise<void> {
  anketaState.submitResume(props.action, resumeForm.value)
  cancelEdit();
}
</script>

<template>
  <UForm :state="resumeForm" @submit.prevent="submitForm">
    <UFormGroup class="mb-3" label="Фамилия" required>
      <UInput
        v-model="resumeForm['surname']"
        placeholder="Фамилия"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя" required>
      <UInput
        v-model="resumeForm['firstname']"
        placeholder="Имя"
      />  
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество">
      <UInput
        v-model="resumeForm['patronymic']"
        placeholder="Отчество"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата рождения" required>
      <UInput
        v-model="resumeForm['birthday']"
        type="date"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Место рождения">
      <UTextarea
        v-model="resumeForm['birthplace']"
        placeholder="Место рождения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Гражданство">
      <UInput
        v-model="resumeForm['citizenship']"
        placeholder="Гражданство"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Двойное гражданство">
      <UInput
        v-model="resumeForm['dual']"
        placeholder="Двойное гражданство"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="СНИЛС">
      <UInput
        v-model="resumeForm['snils']"
        placeholder="СНИЛС"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН">
      <UInput
        v-model="resumeForm['inn']"
        placeholder="ИНН"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Семейное положение">
      <UTextarea
        v-model="resumeForm['marital']"
        placeholder="Семейное положение"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дополнительно">
      <UTextarea
        v-model="resumeForm['addition']"
        placeholder="Дополнительно"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelEdit" />
  </UForm>
</template>
