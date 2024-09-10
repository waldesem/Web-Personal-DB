<script setup lang="ts">
import { useFetchAuth } from "@/utils/auth";
import { server, stateAnketa } from "@/state/state";
import type { Persons } from "@/utils/interfaces";

const authFetch = useFetchAuth();

const anketaState = stateAnketa();

const toast = useToast();

const switchToPersons = async() => {
  navigateTo('/persons');
};

async function submitResume(): Promise<void> {
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
  }
  switchToPersons();
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :div="'mb-6'" :header="'НОВАЯ АНКЕТА'"/>
    <UCard>
      <FormsResumeForm 
        @cancel="switchToPersons"
        @update="/>
    </UCard>
  </LayoutsMenu>
</template>
