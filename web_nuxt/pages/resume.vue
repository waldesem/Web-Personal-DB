<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

const toast = useToast();
const authFetch = useFetchAuth();

const upload = ref(false);
const resume = ref({} as Persons);

const navigateToPersons = () => navigateTo("/persons");

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
}
</script>

<template>
  <div>
    <USkeleton v-if="upload" class="h-44 w-44" />
    <ElementsHeaderDiv
      :div="'mb-6'"
      :header="
        !upload
          ? 'НОВАЯ АНКЕТА'
          : `${resume['surname']} ${resume['firstname']} ${resume['patronymic']}`.toUpperCase()
      "
    />
    <ElementsSkeletonDiv v-if="upload" :rows="16" />
    <ElementsCardDiv v-else>
      <FormsResumeForm @cancel="navigateToPersons" @update="submitResume" />
    </ElementsCardDiv>
  </div>
</template>
