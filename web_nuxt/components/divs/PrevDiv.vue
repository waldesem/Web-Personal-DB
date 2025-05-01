<script setup lang="ts">
import type { Previous } from "@/types";

await preloadComponents("DivsItemsPrevItem");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const prev = ref({} as Previous);
const previous = ref<Previous[]>([]);
const index = ref(0);

const { refresh, status } = await useLazyAsyncData("previous", async () => {
  previous.value = (await useFetchAuth(
    "/route/items/previous/" + candId.value
  )) as Previous[];
});

async function submitPrevious(form: Previous) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
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
  const { message } = (await useFetchAuth(`/route/items/previous/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  index.value = 0;
  if (message == "success") {
    previous.value.splice(idx, 1);
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
    <div v-for="(item, idx) in previous" :key="idx" class="p-1">
      <UCard :variant="status == 'pending' || pending ? 'soft' : 'outline'">
        <div class="flex">
          <div v-if="editable" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="prev" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsPrevItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <div v-if="!previous.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
    <template v-if="editable" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Изменение имени"
        description="Данные профиля"
      >
        <template #content>
          <UCard>
            <FormsPreviousForm
              :previous="prev"
              @cancel="
                prev = {} as Previous;
                modal = false;
              "
              @update="submitPrevious"
            />
          </UCard>
        </template>
      </UModal>
      <UButton
        icon="i-heroicons-document-plus"
        label="Добавить"
        variant="ghost"
        :loading="status == 'pending' || pending"
        @click="
          prev = {} as Previous;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="previous.length > 0 && (status != 'pending' || !pending)"
        @update="
          prev = previous[index];
          modal = true;
        "
        @delete="deletePrevious(previous[index].id, index)"
      />
    </template>
  </UCard>
</template>
