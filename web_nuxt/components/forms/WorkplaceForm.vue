<script setup lang="ts">
import type { Work } from "@/types/interfaces";
import { useDateFormat } from "@vueuse/core";

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
  ? useDateFormat(workForm.value.starts, "YYYY-MM-DD").value
  : "";
workForm.value.finished = workForm.value.finished
  ? useDateFormat(workForm.value.finished, "YYYY-MM-DD").value
  : "";

function submitWorkplace() {
  emit("update", workForm.value);
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
