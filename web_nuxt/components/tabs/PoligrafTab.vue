<script setup lang="ts">
import type { Pfo } from "@/types";

await preloadComponents("DivsPoligrafDiv");
await prefetchComponents("FormsPoligrafForm");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const poligraf = ref({} as Pfo);
const poligrafs = ref<Pfo[]>([]);

const { refresh, status } = await useLazyAsyncData("poligrafs", async () => {
  poligrafs.value = (await useFetchAuth(
    "/route/items/poligrafs/" + candId.value
  )) as Pfo[];
});

async function submitPoligraf(form: Pfo) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
    `/route/items/poligrafs/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  poligraf.value = {} as Pfo;
  await refresh();
  emitMessage(message);
}

async function deletePoligraf(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await useFetchAuth(`/route/items/poligrafs/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    poligrafs.value.splice(idx, 1);
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
      title="Обследование на полиграфе"
      description="Данные профиля"
    >
      <template #content>
        <UCard class="m-2">
          <FormsPoligrafForm
            :poligraf="poligraf"
            @update="submitPoligraf"
            @cancel="
              poligraf = {} as Pfo;
              modal = false;
            "
          />
        </UCard>
      </template>
    </UModal>
    <UCard
      v-for="(item, index) in poligrafs"
      :key="item.id"
      :variant="status == 'pending' || pending ? 'soft' : 'outline'"
      class="m-2"
    >
      <DivsPoligrafDiv :item="item" />
      <template v-if="editable" #footer>
        <ElementsTabMenu
          v-if="poligrafs.length > 0 && (status != 'pending' || !pending)"
          :item="'poligrafs'"
          @cancel="modal = false"
          @update="
            poligraf = item;
            modal = true;
          "
          @delete="deletePoligraf(item.id, index)"
        />
      </template>
    </UCard>
    <div v-if="!poligrafs.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
  </UCard>
</template>
