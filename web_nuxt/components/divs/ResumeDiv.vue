<script setup lang="ts">
import type { Persons } from "@/types";

await preloadComponents("DivsItemsResumeItem");

const emit = defineEmits(["update"]);

const status = inject("status") as Ref<string>;
const person = inject("person") as Ref<Persons>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const resume = ref({} as Persons);

async function submitResume(form: Persons) {
  pending.value = true;
  modal.value = false;
  const { message } = (await useFetchAuth("/route/items/persons", {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  resume.value = {} as Persons;
  emit("update");
  emitMessage(message);
}

async function deleteItem() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  if (!confirm("Данные будут удалены безвозвратно!?")) return;
  pending.value = true;
  const { message } = (await useFetchAuth(
    `/route/items/persons/${person.value.id}`,
    {
      method: "DELETE",
    }
  )) as Record<string, string>;
  pending.value = false;
  emitMessage(message);
  return navigateTo("/persons");
}

const loading = computed(() => {
  return status.value == "pending" || pending.value;
});
</script>

<template>
  <div class="flex flex-col items-center justify-center">
    <UModal
      v-model:open="loading"
      :dismissible="false"
      title="Load"
      description="Loading data"
    >
      <template #content><UProgress animation="swing" /></template>
    </UModal>
  </div>
  <DivsItemsResumeItem :person="person" />
  <div v-if="editable" class="py-2">
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
    <ElementsTabMenu
      :item="'persons'"
      @delete="deleteItem"
      @update="
        resume = person;
        modal = true;
      "
    />
  </div>
  <USeparator />
</template>
