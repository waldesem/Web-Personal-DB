<script setup lang="ts">
import type { Education } from "@/types";

await preloadComponents("DivsItemsEducateItem");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const education = ref({} as Education);
const educations = ref<Education[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("educations", async () => {
  educations.value = (await useFetchAuth(
    "/route/items/educations/" + candId.value
  )) as Education[];
});

async function submitEducation(form: Education) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
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
  const { message } = (await useFetchAuth(`/route/items/educations/${id}`, {
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
    :variant="status == 'pending' || pending ? 'soft' : 'outline'"
    class="my-2 mx-1"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <div v-for="(item, idx) in educations" :key="idx" class="p-1">
      <UCard :variant="status == 'pending' || pending ? 'soft' : 'outline'">
        <div class="flex">
          <div v-if="editable" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="education" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsEducateItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <div v-if="!educations.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
    <template v-if="editable" #footer>
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
        :loading="status == 'pending' || pending"
        @click="
          education = {} as Education;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="educations.length > 0 && (status != 'pending' || !pending)"
        @update="
          education = educations[index];
          modal = true;
        "
        @delete="deleteEducation(educations[index].id, index)"
      />
    </template>
  </UCard>
</template>
