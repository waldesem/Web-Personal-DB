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
  if (state.surname && !state.surname.match(/^[а-яёЁА-Я-\s]+$/)) {
    errors.push({
      path: "surname",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (state.firstname && !state.firstname.match(/^[а-яёЁА-Я-\s]+$/)) {
    errors.push({
      path: "firstname",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (state.patronymic && !state.patronymic.match(/^[а-яёЁА-Я-\s]+$/)) {
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
  if (state.snils && !state.snils.match(/^[0-9]{11}$/)) {
    errors.push({
      path: "snils",
      message: "Поле должно содержать 11 цифр",
    });
  }
  if (state.inn && !state.inn.match(/^[0-9]{12}$/)) {
    errors.push({
      path: "inn",
      message: "Поле должно содержать 12 цифр",
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
    <UFormGroup class="mb-3" label="Фамилия" name="surname">
      <UInput
        v-model.trim="resumeForm['surname']"
        required
        placeholder="Фамилия"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя" name="firstname">
      <UInput
        v-model.trim="resumeForm['firstname']"
        required
        placeholder="Имя"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество" name="patronymic">
      <UInput v-model.trim="resumeForm['patronymic']" placeholder="Отчество" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата рождения" name="birthday">
      <UInput v-model="resumeForm['birthday']" required type="date" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Место рождения">
      <UTextarea
        v-model.trim.lazy="resumeForm['birthplace']"
        placeholder="Место рождения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Гражданство" name="citizenship">
      <UInput
        v-model.trim="resumeForm['citizenship']"
        placeholder="Гражданство"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Двойное гражданство" name="dual">
      <UInput
        v-model.trim="resumeForm['dual']"
        placeholder="Двойное гражданство"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="СНИЛС" name="snils">
      <UInput v-model.trim.lazy="resumeForm['snils']" placeholder="СНИЛС" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН" name="inn">
      <UInput v-model.trim.lazy="resumeForm['inn']" placeholder="ИНН" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Семейное положение" name="marital">
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
