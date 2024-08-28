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
    default: {} as Persons,
  },
});

const anketaState = stateAnketa();

const resumeForm = toRef(props.resume);
resumeForm.value.birthday = resumeForm.value.birthday
  ? new Date(resumeForm.value.birthday).toISOString().slice(0, 10)
  : "";

function cancelEdit() {
  Object.assign(resumeForm.value, {
    surname: "",
    firstname: "",
    patronymic: "",
    birthday: "",
    birthplace: "",
    citizenship: "",
    dual: "",
    inn: "",
    snils: "",
    marital: "",
    addition: "",
  } as Persons);
  emit("cancel");
}

async function submitForm(): Promise<void> {
  anketaState.submitResume(props.action, resumeForm.value);
  cancelEdit();
}
</script>

<template>
  <UForm :state="resumeForm" @submit.prevent="submitForm">
    <UFormGroup class="mb-3" label="Фамилия">
      <UInput v-model="resumeForm['surname']" required placeholder="Фамилия" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя">
      <UInput v-model="resumeForm['firstname']" required placeholder="Имя" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество">
      <UInput v-model="resumeForm['patronymic']" placeholder="Отчество" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата рождения">
      <UInput v-model="resumeForm['birthday']" required type="date" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Место рождения">
      <UTextarea
        v-model="resumeForm['birthplace']"
        placeholder="Место рождения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Гражданство">
      <UInput v-model="resumeForm['citizenship']" placeholder="Гражданство" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Двойное гражданство">
      <UInput v-model="resumeForm['dual']" placeholder="Двойное гражданство" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="СНИЛС">
      <UInput v-model="resumeForm['snils']" placeholder="СНИЛС" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН">
      <UInput v-model="resumeForm['inn']" placeholder="ИНН" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Семейное положение">
      <UTextarea
        v-model="resumeForm['marital']"
        placeholder="Семейное положение"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дополнительно">
      <UTextarea v-model="resumeForm['addition']" placeholder="Дополнительно" />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelEdit" />
  </UForm>
</template>
