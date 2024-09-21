<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  resume: {
    type: Object as () => Persons,
    default: {} as Persons,
  },
});

const resumeForm = toRef(props.resume);

resumeForm.value.birthday = resumeForm.value.birthday
  ? new Date(resumeForm.value.birthday).toISOString().slice(0, 10)
  : "";

function cancelOperation() {
  emit("cancel");
  cancelEdit();
}

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
}

const validate = (state: Persons): FormError[] => {
  const errors = [];
  const pattern = /^[а-яА-Я-\s]+$/;
  if (state.surname && !state.surname.match(pattern)) {
    console.log(state.surname);
    errors.push({
      path: "surname",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (state.firstname && !state.firstname.match(pattern)) {
    console.log(state.firstname);
    errors.push({
      path: "firstname",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (state.patronymic && !state.patronymic.match(pattern)) {
    console.log(state.patronymic);
    errors.push({
      path: "patronymic",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (!Object.prototype.toString.call(state.birthday)) {
    console.log(state.birthday);
    errors.push({
      path: "birthday",
      message: "Поле должно содержать дату",
    });
  }
  if (new Date(state.birthday) > new Date()) {
    console.log(state.birthday);
    errors.push({
      path: "birthday",
      message: "Поле должно содержать корректную дату",
    });
  }
  return errors;
};

async function submitResume() {
  emit("update", resumeForm.value);
  cancelEdit();
}
</script>

<template>
  <UForm
    :state="resumeForm"
    :validate="validate"
    @submit.prevent="submitResume"
  >
    <UFormGroup class="mb-3" label="Фамилия">
      <UInput
        v-model.trim="resumeForm['surname']"
        required
        placeholder="Фамилия"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя">
      <UInput
        v-model.trim="resumeForm['firstname']"
        required
        placeholder="Имя"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество">
      <UInput
        v-model.trim="resumeForm['patronymic']"
        placeholder="Отчество"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата рождения">
      <UInput v-model="resumeForm['birthday']" required type="date" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Место рождения">
      <UTextarea
        v-model.trim.lazy="resumeForm['birthplace']"
        placeholder="Место рождения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Гражданство">
      <UInput
        v-model.trim.lazy="resumeForm['citizenship']"
        placeholder="Гражданство"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Двойное гражданство">
      <UInput
        v-model.trim.lazy="resumeForm['dual']"
        placeholder="Двойное гражданство"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="СНИЛС">
      <UInput v-model.trim.lazy="resumeForm['snils']" placeholder="СНИЛС" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН">
      <UInput v-model.trim.lazy="resumeForm['inn']" placeholder="ИНН" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Семейное положение">
      <UTextarea
        v-model.trim.lazy="resumeForm['marital']"
        placeholder="Семейное положение"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дополнительно">
      <UTextarea
        v-model.trim.lazy="resumeForm['addition']"
        placeholder="Дополнительно"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelOperation" />
  </UForm>
</template>
