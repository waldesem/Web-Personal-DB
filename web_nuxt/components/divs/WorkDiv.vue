<script setup lang="ts">
import type { Work } from "@/types";

await preloadComponents("DivsItemsWorkItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const workplace = ref({} as Work);
const workplaces = ref<Work[]>([]);

const { refresh, status } = await useLazyAsyncData("workplaces", async () => {
  workplaces.value = (await authFetch(
    "/route/items/workplaces/" + candId.value
  )) as Work[];
});

async function submitWorkplace(form: Work) {
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
  if (message == "success") {
    workplaces.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <div v-if="editable || status == 'pending'" class="my-1">
    <UButton
      :loading="status == 'pending' || pending"
      :label="
        status == 'pending' || pending
          ? 'Обновление данных...'
          : 'Добавить запись'
      "
      variant="link"
      @click="modal = !modal"
    />
  </div>
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsWorkplaceForm
        :work="workplace"
        @cancel="
          workplace = {} as Work;
          modal = false;
        "
        @update="submitWorkplace"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in workplaces" :key="idx" class="p-1">
    <ElementsCardDiv>
      <DivsItemsWorkItem :item="item" />
      <template v-if="editable" #footer>
        <ElementsDivMenu
          @delete="deleteWork(item.id, idx)"
          @update="
            workplace = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
