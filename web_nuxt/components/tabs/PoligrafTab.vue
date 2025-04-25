<script setup lang="ts">
import type { Pfo } from "@/types";

await preloadComponents("DivsPoligrafDiv");
await prefetchComponents("FormsPoligrafForm");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const poligraf = ref({} as Pfo);
const poligrafs = ref<Pfo[]>([]);

const { refresh, status } = await useLazyAsyncData("poligrafs", async () => {
  poligrafs.value = (await authFetch(
    "/route/items/poligrafs/" + candId.value
  )) as Pfo[];
});

async function submitPoligraf(form: Pfo) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
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
  const { message } = (await authFetch(`/route/items/poligrafs/${id}`, {
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
    class="m-2"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <div v-if="editable" class="flex justify-between mb-1">
      <UButton
        label="Добавить запись"
        variant="ghost"
        icon="i-heroicons-plus-circle"
        @click="modal = !modal"
      />
      <USwitch
        v-model="edit"
        :label="edit ? 'Отключить редактирование' : 'Включить редактирование'"
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
    <UCard v-for="(item, index) in poligrafs" :key="item.id" class="m-2">
      <DivsPoligrafDiv :item="item" />
      <template v-if="edit" #footer>
        <ElementsTabMenu
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
  </UCard>
</template>
