<script setup lang="ts">
import type { Inquisition } from "@/types";
import { emitMessage } from "@/utils";

prefetchComponents("FormsInvestigationForm");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const inquisition = ref({} as Inquisition);
const investigations = ref<Inquisition[]>([]);

const { refresh, status } = await useLazyAsyncData(
  "investigations",
  async () => {
    investigations.value = (await authFetch(
      "/route/items/investigations/" + candId.value
    )) as Inquisition[];
  }
);

async function submitInvestigations(form: Inquisition) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    "/route/items/investigations/" + candId.value,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  inquisition.value = {} as Inquisition;
  await refresh();
  emitMessage(message);
}

async function deleteInquisition(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/investigations/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    investigations.value.splice(idx, 1);
  }
  emitMessage(message);
}

const items = computed(() =>
  investigations.value.map((item, _) => ({
    label: "Расследование/проверка ID #" + item["id"],
    defaultOpen: true,
    description: item,
  }))
);
</script>

<template>
  <UButton
    v-if="editable"
    :loading="status == 'pending' || pending"
    :label="
      status == 'pending' || pending
        ? 'Обновление данных...'
        : 'Добавить запись'
    "
    variant="link"
    @click="modal = !modal"
  />
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsInvestigationForm
        :investigation="inquisition"
        @cancel="
          inquisition = {} as Inquisition;
          modal = false;
        "
        @update="submitInvestigations"
      />
    </ElementsCardDiv>
  </UModal>
  <UAccordion :items="items" size="lg" multiple>
    <template #item="{ item, index }">
      <ElementsCardDiv>
        <ElementsLabelSlot :label="'Тема проверки'">{{
          item.description["theme"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Информация'">{{
          item.description["info"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item.description["created"]).toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
        <template v-if="editable" #footer>
          <ElementsTabMenu
            :item="'investigations'"
            @cancel="modal = false"
            @update="
              inquisition = item.description;
              modal = true;
            "
            @delete="deleteInquisition(item.description['id'], index)"
          />
        </template>
      </ElementsCardDiv>
    </template>
  </UAccordion>
</template>
