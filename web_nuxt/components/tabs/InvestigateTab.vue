<script setup lang="ts">
import type { Inquisition } from "@/types";

await preloadComponents("DivsInvestigateDiv");
await prefetchComponents("FormsInvestigationForm");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const inquisition = ref({} as Inquisition);
const investigations = ref<Inquisition[]>([]);

const { refresh, status } = await useLazyAsyncData(
  "investigations",
  async () => {
    investigations.value = (await useFetchAuth(
      "/route/items/investigations/" + candId.value
    )) as Inquisition[];
  }
);

async function submitInvestigations(form: Inquisition) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
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
  const { message } = (await useFetchAuth(`/route/items/investigations/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    investigations.value.splice(idx, 1);
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
    <div v-if="editable" class="flex justify-between mb-1 me-2">
      <UButton
        label="Добавить запись"
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
    <UCard
      v-for="(item, index) in investigations"
      :key="item.id"
      :variant="status == 'pending' || pending ? 'soft' : 'outline'"
      class="m-2"
    >
      <DivsInvestigateDiv :item="item" />
      <template v-if="editable" #footer>
        <ElementsTabMenu
          v-if="investigations.length > 0 && (status != 'pending' || !pending)"
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
    <div v-if="!investigations.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
  </UCard>
</template>
