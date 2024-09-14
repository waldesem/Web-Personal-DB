<script setup lang="ts">
import { useFetchAuth } from "@/utils/auth";
import { server } from "@/state/state";
import type { Persons } from "@/types/interfaces";

const authFetch = useFetchAuth();

const toast = useToast();

async function submitResume(form: Persons): Promise<void> {
  const response = await authFetch(`${server}/resume`, {
    method: "POST",
    body: form,
  });
  console.log(response);
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: `Данные успешно добавлены`,
    color: "green",
  });
  navigateTo('/persons');
}
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :div="'mb-6'" :header="'НОВАЯ АНКЕТА'"/>
    <UCard>
      <FormsResumeForm 
        @cancel="navigateTo('/persons')"
        @update="submitResume" />
    </UCard>
  </LayoutsMenu>
</template>
