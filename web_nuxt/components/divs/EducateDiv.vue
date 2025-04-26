<script setup lang="ts">
import type { Education } from "@/types";

await preloadComponents("DivsItemsEducateItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const education = ref({} as Education);
const educations = ref<Education[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("educations", async () => {
  educations.value = (await authFetch(
    "/route/items/educations/" + candId.value
  )) as Education[];
});

async function submitEducation(form: Education) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/educations/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  education.value = {} as Education;
  await refresh();
  emitMessage(message);
}

async function deleteEducation(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/educations/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  index.value = 0;
  if (message == "success") {
    educations.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <UCard
    class="m-2"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <USwitch
      v-if="editable"
      v-model="edit"
      :label="edit ? 'Отключить редактирование' : 'Включить редактирование'"
      size="xs"
      class="mb-2 me-2 justify-end"
    />
    <div v-for="(item, idx) in educations" :key="idx" class="p-1">
      <UCard>
        <div class="flex">
          <div v-if="edit" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="education" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsEducateItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <template v-if="edit" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Образование"
        description="Данные профиля"
      >
        <template #content>
          <UCard>
            <FormsEducationForm
              :education="education"
              @cancel="
                education = {} as Education;
                modal = false;
              "
              @update="submitEducation"
            />
          </UCard>
        </template>
      </UModal>
      <UButton
        icon="i-heroicons-document-plus"
        label="Добавить"
        variant="ghost"
        @click="
          education = {} as Education;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="educations.length > 0"
        @update="
          education = educations[index];
          modal = true;
        "
        @delete="deleteEducation(educations[index].id, index)"
      />
    </template>
  </UCard>
</template>
