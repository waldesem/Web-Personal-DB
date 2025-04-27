<script setup lang="ts">
import type { Persons } from "@/types";

await preloadComponents("DivsItemsResumeItem");

const emit = defineEmits(["update"]);

const status = inject("status") as Ref<string>;
const person = inject("person") as Ref<Persons>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
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
</script>

<template>
  <UCard
    class="my-2 mx-1"
    :class="{ 'animate-pulse': pending }"
  >
    <USwitch
      v-if="editable"
      v-model="edit"
      :label="edit ? 'Отключить редактирование' : 'Включить редактирование'"
      size="xs"
      class="mb-2 me-2 justify-end"
    />
    <div v-if="status === 'pending'">
      <div v-for="i in 14" :key="i" class="flex grid grid-cols-12 gap-3 mb-3">
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
    <template v-if="edit" #footer>
      <UModal
        v-model:open="modal"
        :ui="{ content: 'overflow-y-auto' }"
        :dismissible="false"
        title="Резюме"
        description="Данные профиля"
      >
        <template #content>
          <UCard class="m-2">
            <FormsResumeForm
              :resume="resume"
              @update="submitResume"
              @cancel="
                resume = {} as Persons;
                modal = false;
              "
            />
          </UCard>
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
    </template>
  </UCard>
</template>
