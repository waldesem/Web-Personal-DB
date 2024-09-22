<script setup lang="ts">
import { useFetchAuth } from "@/utils/auth";
import type { Persons } from "@/types/interfaces";

const toast = useToast();

const authFetch = useFetchAuth();

function openPersons() {
  return navigateTo("/persons");
}

async function submitResume(form: Persons) {
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
  return navigateTo("/profile/" + person_id);
}
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :div="'mb-6'" :header="'НОВАЯ АНКЕТА'" />
    <ElementsCardDiv>
      <FormsResumeForm @cancel="openPersons" @update="submitResume" />
    </ElementsCardDiv>
  </LayoutsMenu>
</template>
