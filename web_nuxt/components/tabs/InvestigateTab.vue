<script setup lang="ts">
import type { Inquisition } from "@/types";

await preloadComponents("DivsInvestigateDiv");
await prefetchComponents("FormsInvestigationForm");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const inquisition = ref({} as Inquisition);
const investigations = ref<Inquisition[]>([]);

const { refresh, status } = await useLazyAsyncData(
  "investigations",
  async () => {
    investigations.value = (await authFetch(
      "/route/items/investigations/" + candId.value
    )) as Inquisition[];
  }
);

async function submitInvestigations(form: Inquisition) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    "/route/items/investigations/" + candId.value,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  inquisition.value = {} as Inquisition;
  await refresh();
  emitMessage(message);
}

async function deleteInquisition(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/investigations/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    investigations.value.splice(idx, 1);
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
      variant="ghost"
      icon="i-heroicons-plus-circle"
      @click="modal = !modal"
    />
  </div>
  <UModal
    v-model:open="modal"
    :ui="{ content: 'sm:max-w-4xl overflow-y-auto' }"
    :dismissible="false"
    title="Расследование"
    description="Данные профиля"
  >
    <template #content>
       <UCard class="m-2">
        <FormsInvestigationForm
          :investigation="inquisition"
          @cancel="
            inquisition = {} as Inquisition;
            modal = false;
          "
          @update="submitInvestigations"
        />
      </UCard>
    </template>
  </UModal>
   <UCard v-for="(item, index) in investigations" :key="item.id" class="m-2">
    <DivsInvestigateDiv :item="item" />
    <template v-if="editable" #footer>
      <ElementsTabMenu
        :item="'investigations'"
        @cancel="modal = false"
        @delete="deleteInquisition(item.id, index)"
        @update="
          inquisition = item;
          modal = true;
        "
      />
    </template>
  </UCard>
</template>
