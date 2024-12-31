<script setup lang="ts">
import type { Persons } from "@/types";

prefetchComponents("FormsResumeForm");

const toast = useToast();
const authFetch = useFetchAuth();

const upload = ref(true);

const navigateToPersons = () => navigateTo("/persons");

async function submitResume(form: Persons) {
  upload.value = true;
  const { person_id } = (await authFetch("/route/anketa/resume", {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  if (person_id) {
    return navigateTo("/profile/" + person_id);
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
  <div class="mb-6">
    <ElementsHeaderDiv v-if="!upload" header="НОВАЯ АНКЕТА" />
    <div class="text-center py-32">
      <UIcon
        v-if="upload"
        :name="'i-heroicons-arrow-path'"
        class="animate-spin w-16 h-16 text-gray-600 dark:text-gray-200"
      />
      <ElementsCardDiv v-else>
        <FormsResumeForm @cancel="navigateToPersons" @update="submitResume" />
      </ElementsCardDiv>
    </div>
  </div>
</template>
