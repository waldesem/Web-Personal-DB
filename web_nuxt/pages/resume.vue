<script setup lang="ts">
import type { Persons } from "@/types";

prefetchComponents("FormsResumeForm");

const toast = useToast();
const authFetch = useFetchAuth();

const upload = ref(false);

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
    <USkeleton v-if="upload" class="my-6 h-8 w-1/3" />
    <ElementsHeaderDiv v-else header="НОВАЯ АНКЕТА" />
    <ElementsSkeletonDiv v-if="upload" :rows="18" />
    <ElementsCardDiv v-else>
      <FormsResumeForm @cancel="navigateToPersons" @update="submitResume" />
    </ElementsCardDiv>
  </div>
</template>
