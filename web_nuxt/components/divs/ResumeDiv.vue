<script setup lang="ts">
import type { Persons } from "@/types";

await preloadComponents("DivsItemsResumeItem");

const emit = defineEmits(["update"]);

const status = inject("status") as Ref<string>;
const person = inject("person") as Ref<Persons>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const resume = ref({} as Persons);

async function submitResume(form: Persons) {
  modal.value = false;
  status.value = "pending";
  const { message } = (await useFetchAuth("/route/items/persons", {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  status.value = "success";
  resume.value = {} as Persons;
  emit("update");
  emitMessage(message);
}

async function deleteItem() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  if (!confirm("Данные будут удалены безвозвратно!?")) return;
  status.value = "pending";
  const { message } = (await useFetchAuth(
    `/route/items/persons/${person.value.id}`,
    {
      method: "DELETE",
    }
  )) as Record<string, string>;
  status.value = "success";
  emitMessage(message);
  return navigateTo("/persons");
}
</script>

<template>
  <div v-if="editable" class="relative">
    <div class="absolute top-2 right-2">
      <ElementsTabMenu
        :item="'persons'"
        @delete="deleteItem"
        @update="
          resume = person;
          modal = true;
        "
      />
    </div>
  </div>
  <div v-if="status === 'pending'">
    <div 
      v-for="p in Object.keys(person)" 
      :key="p" 
      class="flex grid grid-cols-12 gap-3 mb-3"
    >
      <div class="col-span-3">
        <USkeleton class="h-4" />
      </div>
      <div class="col-span-9">
        <USkeleton class="h-4 w-[300px]" />
      </div>
    </div>
  </div>
  <div v-else>
    <DivsItemsResumeItem :person="person" />
  </div>
  <UModal
    v-model:open="modal"
    :ui="{ content: 'overflow-y-auto' }"
    :dismissible="false"
    title="Резюме"
    description="Данные профиля"
  >
    <template #content>
      <div class="m-4">
        <FormsResumeForm
          :resume="resume"
          @update="submitResume"
          @cancel="
            resume = {} as Persons;
            modal = false;
          "
        />
      </div>
    </template>
  </UModal>
  <USeparator />
</template>
