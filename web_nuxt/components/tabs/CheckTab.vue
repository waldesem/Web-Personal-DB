<script setup lang="ts">
import type { Verification } from "@/types";

await preloadComponents("DivsCheckDiv");
await prefetchComponents("FormsCheckForm");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const check = ref({} as Verification);
const checks = ref<Verification[]>([]);

const { refresh, status } = await useLazyAsyncData("checks", async () => {
  checks.value = (await useFetchAuth(
    `/route/items/checks/${candId.value}`
  )) as Verification[];
});

async function submitCheck(form: Verification) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
    `/route/items/checks/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  check.value = {} as Verification;
  await refresh();
  emitMessage(message);
}

async function deleteCheck(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await useFetchAuth(`/route/items/checks/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    checks.value.splice(idx, 1);
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
    <UModal
      v-model:open="modal"
      :ui="{ content: 'sm:max-w-4xl overflow-y-auto' }"
      :dismissible="false"
      title="Проверка кандидата"
      description="Данные профиля"
    >
      <template #content>
        <UCard class="m-2">
          <FormsCheckForm
            :check="check"
            @cancel="
              check = {} as Verification;
              modal = false;
            "
            @update="submitCheck"
          />
        </UCard>
      </template>
    </UModal>
    <UButton
      :loading="status == 'pending' || pending"
      label="Добавить запись"
      variant="ghost"
      icon="i-heroicons-plus-circle"
      @click="modal = !modal"
    />
    <UCard
      v-for="(item, index) in checks"
      :key="item.id"
      :variant="status == 'pending' || pending ? 'soft' : 'outline'"
      class="m-2"
    >
      <DivsCheckDiv :item="item" />
      <template v-if="editable" #footer>
        <ElementsTabMenu
          v-if="checks.length > 0 && (status != 'pending' || !pending)"
          :item="'checks'"
          @cancel="modal = false"
          @delete="deleteCheck(item.id, index)"
          @update="
            check = item;
            modal = true;
          "
        />
      </template>
    </UCard>
    <div v-if="!checks.length" class="flex justify-center text-red-800">
      <div v-if="status == 'pending' || pending">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin w-8 h-8" />
      </div>
      <div v-else>Данные отсутствуют</div>
    </div>
  </UCard>
</template>
