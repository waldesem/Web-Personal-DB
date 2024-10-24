<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

const toast = useToast();
const authFetch = useFetchAuth();

const upload = ref(false);

const navigateToPersons = () => navigateTo("/persons");

async function submitResume(form: Persons) {
  upload.value = true;
  const { person_id } = (await authFetch("/api/resume", {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  if (person_id) {
    await navigateTo("/profile/" + person_id);
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Невозможно выполнить действие",
      color: "red",
    });
  }
  upload.value = false;
}
</script>

<template>
  <div v-if="upload">
    <USkeleton class="h-44 w-44" />
    <USkeleton class="mb-6 h-16 w-96" />
    <ElementsSkeletonDiv :rows="16" />
  </div>
  <div v-else>
    <ElementsHeaderDiv :div="'mb-6'" header="НОВАЯ АНКЕТА" />
    <ElementsCardDiv>
      <FormsResumeForm @cancel="navigateToPersons" @update="submitResume" />
    </ElementsCardDiv>
  </div>
</template>
