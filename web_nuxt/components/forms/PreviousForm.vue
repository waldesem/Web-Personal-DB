<script setup lang="ts">
import type { Previous } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  previous: {
    type: Object as () => Previous,
    default: {} as Previous,
  },
  candId: {
    type: String,
    default: "",
  },
});

const previousForm = toRef(props.previous as Previous);

async function submitPrevious() {
  emit("cancel");
  await authFetch("/api/previous/" + props.candId, {
    method: "POST",
    body: previousForm.value,
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
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
