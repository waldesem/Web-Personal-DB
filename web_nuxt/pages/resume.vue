<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

const toast = useToast();
const authFetch = useFetchAuth();

const upload = ref(false);
const resume = ref({}l as Persons;
function openPersons() {
  return navigateTo("/persons");
}

async function submitResume(form: Persons) {
  resume.value = form;
  upload.value = true;
  const { person_id } = (await authFetch("/api/resume", {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация добавлена",
    color: "green",
  });
  upload.value = false;
  refreshNuxtData("candidates");
  return navigateTo("/profile/" + person_id);
}
</script>

<template>
  <div>
    <ElementsHeaderDiv :div="'mb-6'" :header="!upload ? 'НОВАЯ АНКЕТА' : `${resume['surname']} {resume['firstname']} {resume['patronymic']}`.toUpperCase()" />
    <ElementsSkeletonDiv v-if="upload" :rows="16" />
    <ElementsCardDiv v-else>
      <FormsResumeForm @cancel="openPersons" @update="submitResume" />
    </ElementsCardDiv>
  </div>
</template>
