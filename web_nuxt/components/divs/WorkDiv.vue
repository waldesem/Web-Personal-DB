<script setup lang="ts">
import type { Work } from "@/types";

await preloadComponents("DivsItemsWorkItem");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const workplace = ref({} as Work);
const workplaces = ref<Work[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("workplaces", async () => {
  workplaces.value = (await useFetchAuth(
    "/route/items/workplaces/" + candId.value
  )) as Work[];
});

async function submitWork(form: Work) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
    `/route/items/workplaces/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  workplace.value = {} as Work;
  await refresh();
  emitMessage(message);
}

async function deleteWork(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await useFetchAuth(`/route/items/workplaces/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  index.value = 0;
  if (message == "success") {
    workplaces.value.splice(idx, 1);
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
    <div v-for="(item, idx) in workplaces" :key="idx" class="p-1">
      <UCard :variant="status == 'pending' || pending ? 'soft' : 'outline'">
        <div class="flex">
          <div v-if="editable" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="workplace" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsWorkItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <div v-if="!workplaces.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
    <template v-if="editable" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Место работы"
        description="Данные профиля"
      >
        <template #content>
          <UCard>
            <FormsWorkplaceForm
              :work="workplace"
              @cancel="
                workplace = {} as Work;
                modal = false;
              "
              @update="submitWork"
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
          workplace = {} as Work;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="workplaces.length > 0 && (status != 'pending' || !pending)"
        @update="
          workplace = workplaces[index];
          modal = true;
        "
        @delete="deleteWork(workplaces[index].id, index)"
      />
    </template>
  </UCard>
</template>
