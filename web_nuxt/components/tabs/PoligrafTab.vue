<script setup lang="ts">
import type { Pfo } from "@/types";

await preloadComponents("DivsPoligrafDiv");
await prefetchComponents("FormsPoligrafForm");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

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
  <UModal
    v-model:open="modal"
    :ui="{ content: 'sm:max-w-4xl' }"
    :dismissible="false"
    title="Обследование на полиграфе"
    description="Данные профиля"
  >
    <template #content>
      <ElementsCardDiv>
        <FormsPoligrafForm
          :poligraf="poligraf"
          @update="submitPoligraf"
          @cancel="
            poligraf = {} as Pfo;
            modal = false;
          "
        />
      </ElementsCardDiv>
    </template>
  </UModal>
  <ElementsCardDiv v-for="(item, index) in poligrafs" :key="item.id">
    <DivsPoligrafDiv :item="item" />
    <template v-if="editable" #footer>
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
  </ElementsCardDiv>
</template>
