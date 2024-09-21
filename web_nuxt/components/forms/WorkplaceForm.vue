<script setup lang="ts">
import type { Work } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  work: {
    type: Object as () => Work,
    default: {} as Work,
  },
  candId: {
    type: String,
    default: "",
  },
});

const workForm = toRef(props.work as Work);

workForm.value.starts = workForm.value.starts
  ? new Date(workForm.value.starts).toISOString().slice(0, 10)
  : "";
workForm.value.finished = workForm.value.finished
  ? new Date(workForm.value.finished).toISOString().slice(0, 10)
  : "";

async function submitWorkplace() {
  emit("cancel");
  await authFetch("/api/workplaces/" + props.candId, {
    method: "POST",
    body: workForm.value,
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
  Object.assign(workForm.value, {
    now_work: false,
    starts: "",
    finished: "",
    workplace: "",
    position: "",
    addresses: "",
    reason: "",
  } as Work);
}
</script>

<template>
  <UForm :state="workForm" @submit.prevent="submitWorkplace">
    <UFormGroup class="mb-3" label="Текущая работа">
      <UCheckbox v-model="workForm['now_work']" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Начало работы">
      <UInput
        v-model="workForm['starts']"
        required
        placeholder="Начало работы"
        type="date"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Окончание работы">
      <UInput
        v-model="workForm['finished']"
        required
        placeholder="Окончание работы"
        type="date"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Место работы">
      <UInput
        v-model.trim.lazy="workForm['workplace']"
        required
        placeholder="Место работы"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Должность">
      <UInput
        v-model.trim.lazy="workForm['position']"
        required
        placeholder="Должность"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Адрес организации">
      <UInput
        v-model.trim.lazy="workForm['addresses']"
        placeholder="Адрес организации"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Причина увольнения">
      <UInput
        v-model.trim.lazy="workForm['reason']"
        placeholder="Причина увольнения"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
