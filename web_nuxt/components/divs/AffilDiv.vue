<script setup lang="ts">
import type { Affilation } from "@/types";

await preloadComponents("DivsItemsAffilItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const affilation = ref({} as Affilation);
const affilations = ref<Affilation[]>([]);

const { refresh, status } = await useLazyAsyncData("affilations", async () => {
  affilations.value = (await authFetch(
    "/route/items/affilations/" + candId.value
  )) as Affilation[];
});

async function submitAffilation(form: Affilation) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/affilations/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  affilation.value = {} as Affilation;
  await refresh();
  emitMessage(message);
}

async function deleteAffilation(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/affilations/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  if (message == "success") {
    affilations.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template><ElementsCardDiv>
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
    :dismissible="false"
    title="Аффилированность"
    description="Данные профиля"
  >
    <template #content>
      <ElementsCardDiv>
        <FormsAffilationForm
          :affil="affilation"
          @cancel="
            affilation = {} as Affilation;
            modal = false;
          "
          @update="submitAffilation"
        />
      </ElementsCardDiv>
    </template>
  </UModal>
  <div v-for="(item, idx) in affilations" :key="idx" class="p-1">
    <ElementsCardDiv>
      <DivsItemsAffilItem :item="item" />
      <template v-if="editable" #footer>
        <ElementsDivMenu
          @delete="deleteAffilation(item.id, idx)"
          @update="
            affilation = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div></ElementsCardDiv>
</template>
