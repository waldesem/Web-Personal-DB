<script setup lang="ts">
import type { Work } from "@/types";

await preloadComponents("DivsItemsWorkItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const workplace = ref({} as Work);
const workplaces = ref<Work[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("workplaces", async () => {
  workplaces.value = (await authFetch(
    "/route/items/workplaces/" + candId.value
  )) as Work[];
});

async function submitWork(form: Work) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
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
  const { message } = (await authFetch(`/route/items/workplaces/${id}`, {
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
    class="my-2 mx-1"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <USwitch
      v-if="editable"
      v-model="edit"
      :label="edit ? 'Отключить редактирование' : 'Включить редактирование'"
      size="xs"
      class="mb-2 me-2 justify-end"
    />
    <div v-for="(item, idx) in workplaces" :key="idx" class="p-1">
      <UCard>
        <div class="flex">
          <div v-if="edit" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="workplace" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsWorkItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <template v-if="edit" #footer>
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
        @click="
          workplace = {} as Work;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="workplaces.length > 0"
        @update="
          workplace = workplaces[index];
          modal = true;
        "
        @delete="deleteWork(workplaces[index].id, index)"
      />
    </template>
  </UCard>
</template>
