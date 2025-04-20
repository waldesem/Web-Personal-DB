<script setup lang="ts">
import type { Verification } from "@/types";

await preloadComponents("DivsCheckDiv");
await prefetchComponents("FormsCheckForm");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

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

const items = computed(() =>
  checks.value.map((item, _) => ({
    label: "Проверка кандидата ID #" + item["id"],
    defaultOpen: true,
    description: item,
  }))
);
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
  <UModal v-model:open="modal" :dismissible="false" :ui="{ content: 'sm:max-w-4xl' }">
    <ElementsCardDiv>
      <FormsCheckForm
        :check="check"
        @cancel="
          check = {} as Verification;
          modal = false;
        "
        @update="submitCheck"
      />
    </ElementsCardDiv>
  </UModal>
  <UAccordion :items="items" size="lg" multiple>
    <template #body="{ item, index }">
      <ElementsCardDiv>
        <DivsCheckDiv :item="item.description" />
        <template v-if="editable" #footer>
          <ElementsTabMenu
            :item="'checks'"
            @cancel="modal = false"
            @delete="deleteCheck(item.description.id, index)"
            @update="
              check = item.description;
              modal = true;
            "
          />
        </template>
      </ElementsCardDiv>
    </template>
  </UAccordion>
</template>
