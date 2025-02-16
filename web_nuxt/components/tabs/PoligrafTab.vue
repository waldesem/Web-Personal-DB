<script setup lang="ts">
import type { Pfo } from "@/types";

prefetchComponents("FormsPoligrafForm");

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

const items = computed(() =>
  poligrafs.value.map((item, _) => ({
    label: "Обследование на полиграфе ID #" + item["id"],
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
  <UModal v-model="modal" prevent-close>
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
  </UModal>
  <UAccordion :items="items" size="lg" multiple>
    <template #item="{ item, index }">
      <ElementsCardDiv>
        <DivsPoligrafDiv :item="item.description" />
        <template v-if="editable" #footer>
          <ElementsTabMenu
            :item="'poligrafs'"
            @cancel="modal = false"
            @update="
              poligraf = item.description;
              modal = true;
            "
            @delete="deletePoligraf(item.description.id, index)"
          />
        </template>
      </ElementsCardDiv>
    </template>
  </UAccordion>
</template>
