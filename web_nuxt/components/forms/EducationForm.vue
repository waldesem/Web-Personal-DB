<script setup lang="ts">
import type { Education } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["cancel", "close", "update"]);

const props = defineProps({
  education: {
    type: Object as () => Education,
    default: {} as Education,
  },
  candId: {
    type: String,
    default: "",
  },
});

const educationForm = toRef(props.education as Education);

function submitEducation() {
  emit("close");
  authFetch("/api/educations/" + props.candId, {
    method: "POST",
    body: educationForm.value,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  emit("update");
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(educationForm.value, {
    view: "",
    institution: "",
    finished: "",
    specialty: "",
  } as Education);
}
</script>

<template>
  <UForm :state="educationForm" @submit.prevent="submitEducation">
    <UFormGroup class="mb-3" label="Вид образования">
      <USelect
        v-model="educationForm['view']"
        required
        :options="[
          'Основное общее',
          'Среднее общее',
          'Среднее профессиональное',
          'Высшее',
          'Неоконченное высшее образование',
          'Другое образование',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Название учебного заведения">
      <UInput
        v-model.trim.lazy="educationForm['institution']"
        required
        placeholder="Название учебного заведения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Год окончания">
      <UInput
        v-model.trim.lazy="educationForm['finished']"
        placeholder="Год окончания"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Специальность">
      <UInput
        v-model.trim.lazy="educationForm['specialty']"
        placeholder="Специальность"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
