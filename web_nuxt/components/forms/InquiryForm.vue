<script setup lang="ts">
import type { Needs } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {} as Needs,
  },
  candId: {
    type: String,
    default: "",
  },
});

const inquiryForm = toRef(props.inquiry as Needs);

async function submitIquiry() {
  emit("cancel");
  await authFetch("/api/inquiries/" + props.candId, {
    method: "POST",
    body: inquiryForm.value,
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
  Object.assign(inquiryForm.value, {
    info: "",
    origins: "",
    initiator: "",
  } as Needs);
}
</script>

<template>
  <UForm :state="inquiryForm" @submit.prevent="submitIquiry">
    <UFormGroup class="mb-3" label="Информация">
      <UTextarea
        v-model.trim.lazy="inquiryForm['info']"
        required
        placeholder="Информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Инициатор">
      <UInput
        v-model.trim.lazy="inquiryForm['initiator']"
        required
        placeholder="Инициатор"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Источники">
      <UInput
        v-model.trim.lazy="inquiryForm['origins']"
        placeholder="Источники"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
