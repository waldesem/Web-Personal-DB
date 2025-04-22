<script setup lang="ts">
import type { Previous } from "@/types";

await preloadComponents("DivsItemsPrevItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const prev = ref({} as Previous);
const previous = ref<Previous[]>([]);

const { refresh, status } = await useLazyAsyncData("previous", async () => {
  previous.value = (await authFetch(
    "/route/items/previous/" + candId.value
  )) as Previous[];
});

async function submitPrevious(form: Previous) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/previous/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  prev.value = {} as Previous;
  await refresh();
  emitMessage(message);
}

async function deletePrevious(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/previous/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  if (message == "success") {
    previous.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <UCollapsible class="m-2">
    <UButton
      label="Изменения имени"
      icon="i-heroicons-user"
      color="neutral"
      variant="subtle"
      trailing-icon="i-lucide-chevron-down"
      block
    />
    <template #content>
      <ElementsCardDiv>
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
          title="Предыдущие работы"
          description="Данные профиля"
        >
          <template #content>
            <ElementsCardDiv>
              <FormsPreviousForm
                :prev="prev"
                @cancel="
                  prev = {} as Previous;
                  modal = false;
                "
                @update="submitPrevious"
              />
            </ElementsCardDiv>
          </template>
        </UModal>
        <div v-for="(item, idx) in previous" :key="idx" class="p-1">
          <ElementsCardDiv>
            <DivsItemsPrevItem :item="item" />
            <template v-if="editable" #footer>
              <ElementsDivMenu
                @delete="deletePrevious(item.id, idx)"
                @update="
                  prev = item;
                  modal = true;
                "
              />
            </template>
          </ElementsCardDiv>
        </div>
      </ElementsCardDiv>
    </template>
  </UCollapsible>
</template>
