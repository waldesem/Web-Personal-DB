<script setup lang="ts">
import type { Affilation } from "@/types";

await preloadComponents("DivsItemsAffilItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const affilation = ref({} as Affilation);
const affilations = ref<Affilation[]>([]);
const index = ref(0);

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
  index.value = 0;
  if (message == "success") {
    affilations.value.splice(idx, 1);
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
    <div v-for="(item, idx) in affilations" :key="idx" class="p-1">
      <UCard>
        <div class="flex">
          <div v-if="edit" class="flex-none mr-6 self-center">
            <input
              v-model="index"
              type="radio"
              name="affilation"
              :value="idx"
            >
          </div>
          <div class="flex-grow">
            <DivsItemsAffilItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <template v-if="edit" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Аффилированность"
        description="Данные профиля"
      >
        <template #content>
          <UCard>
            <FormsAffilationForm
              :affilation="affilation"
              @cancel="
                affilation = {} as Affilation;
                modal = false;
              "
              @update="submitAffilation"
            />
          </UCard>
        </template>
      </UModal>
      <UButton
        icon="i-heroicons-document-plus"
        label="Добавить"
        variant="ghost"
        @click="
          affilation = {} as Affilation;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="affilations.length > 0"
        @update="
          affilation = affilations[index];
          modal = true;
        "
        @delete="deleteAffilation(affilations[index].id, index)"
      />
    </template>
  </UCard>
</template>
