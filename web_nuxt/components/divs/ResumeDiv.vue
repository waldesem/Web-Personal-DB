<script setup lang="ts">
import type { Persons } from "@/types";

const emit = defineEmits(["update"]);

const authFetch = useFetchAuth();

const status = inject("status") as Ref<string>;
const person = inject("person") as Ref<Persons>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const resume = ref({} as Persons);

async function submitResume(form: Persons) {
  pending.value = true;
  modal.value = false;
  const { message } = (await authFetch("/route/items/persons", {
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
  const { message } = (await authFetch(
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
  <ElementsCardDiv>
    <UModal v-model="modal" prevent-close>
      <ElementsCardDiv>
        <FormsResumeForm
          :resume="resume"
          @update="submitResume"
          @cancel="
            resume = {} as Persons;
            modal = false;
          "
        />
      </ElementsCardDiv>
    </UModal>
    <div v-if="pending || status === 'pending'">
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
      <DivsItemsResumeItem :item="person" />
    </div>
    <template v-if="editable" #footer>
      <ElementsTabMenu
        :item="'persons'"
        @delete="deleteItem"
        @update="
          resume = person;
          modal = true;
        "
      />
    </template>
  </ElementsCardDiv>
</template>
