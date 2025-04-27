<script setup lang="ts">
import type { Needs } from "@/types";

await preloadComponents("DivsInquiryDiv");
await prefetchComponents("FormsInquiryForm");

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const need = ref({} as Needs);
const inquiries = ref<Needs[]>([]);

const { refresh, status } = await useLazyAsyncData("inquiries", async () => {
  inquiries.value = (await useFetchAuth(
    `/route/items/inquiries/${candId.value}`
  )) as Needs[];
});

async function submitIquiry(form: Needs) {
  modal.value = false;
  pending.value = true;
  const { message } = (await useFetchAuth(
    `/route/items/inquiries/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  need.value = {} as Needs;
  await refresh();
  emitMessage(message);
}

async function deleteNeed(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await useFetchAuth(`/route/items/inquiries/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    inquiries.value.splice(idx, 1);
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
      title="Запрос"
      description="Данные профиля"
    >
      <template #content>
        <UCard class="m-2">
          <FormsInquiryForm
            :inquiry="need"
            @cancel="
              need = {} as Needs;
              modal = false;
            "
            @update="submitIquiry"
          />
        </UCard>
      </template>
    </UModal>
    <UCard v-for="(item, index) in inquiries" :key="item.id" class="m-2">
      <DivsInquiryDiv :item="item" />
      <template v-if="edit" #footer>
        <ElementsTabMenu
          :item="'inquiries'"
          @cancel="modal = false"
          @delete="deleteNeed(item.id, index)"
          @update="
            need = item;
            modal = true;
          "
        />
      </template>
    </UCard>
  </UCard>
</template>
