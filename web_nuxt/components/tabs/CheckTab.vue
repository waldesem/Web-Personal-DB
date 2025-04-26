<script setup lang="ts">
import type { Verification } from "@/types";

await preloadComponents("DivsCheckDiv");
await prefetchComponents("FormsCheckForm");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const check = ref({} as Verification);
const checks = ref<Verification[]>([]);

const { refresh, status } = await useLazyAsyncData("checks", async () => {
  checks.value = (await authFetch(
    `/route/items/checks/${candId.value}`
  )) as Verification[];
});

async function submitCheck(form: Verification) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/checks/${candId.value}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  check.value = {} as Verification;
  await refresh();
  emitMessage(message);
}

async function deleteCheck(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/checks/${id}`, {
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
    class="my-2 mx-1"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <div v-if="editable" class="flex justify-between mb-1 me-2">
      <UButton
        :loading="status == 'pending' || pending"
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
    <UCard v-for="(item, index) in checks" :key="item.id" class="m-2">
      <DivsCheckDiv :item="item" />
      <template v-if="edit" #footer>
        <ElementsTabMenu
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
  </UCard>
</template>
