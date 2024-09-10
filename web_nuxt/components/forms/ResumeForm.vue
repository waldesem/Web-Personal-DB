<script setup lang="ts">
import { useFetchAuth } from "@/utils/auth";
import { server, stateAnketa } from "@/state/state";
import type { Persons } from "@/utils/interfaces";

const authFetch = useFetchAuth();

const anketaState = stateAnketa();

const toast = useToast();

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


const resumeForm = toRef(props.resume);

resumeForm.value.birthday = resumeForm.value.birthday
  ? new Date(resumeForm.value.birthday).toISOString().slice(0, 10)
  : "";

function cancelOperation() {
  emit('cancel')
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

async function submitResume(): Promise<void> {
  emit('cancel')
  if (props.action == "create") {
    const response = await authFetch(`${server}/resume`, {
      method: "POST",
      body: resumeForm.value,
    });
    console.log(response);
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: `Данные успешно добавлены`,
      color: "green",
    });
  } else {
    Promise.all([
      anketaState.updateItem("persons", resumeForm.value),
      anketaState.getItem('persons')
])
  }
  cancelEdit();
}
</script>

<template>
  <UForm :state="resumeForm" @submit.prevent="submitResume">
    <UFormGroup class="mb-3" label="Фамилия">
      <UInput
        v-model.trim.lazy="resumeForm['surname']"
        required
        placeholder="Фамилия"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя">
      <UInput
        v-model.trim.lazy="resumeForm['firstname']"
        required
        placeholder="Имя"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество">
      <UInput
        v-model.trim.lazy="resumeForm['patronymic']"
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
