<script setup lang="ts">
import type { Pfo } from "@/types";
import { emitMessage } from "@/utils";

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
  <div
    v-for="(item, index) in poligrafs"
    :key="index"
    class="text-sm text-gray-500 dark:text-gray-400 py-1"
  >
    <ElementsCardDiv>
      <template #header>
        <div class="tex-base text-red-800 font-medium">
          {{ "Обследование на полиграфе ID #" + item["id"] }}
        </div>
      </template>
      <ElementsLabelSlot v-if="item['theme']" :label="'Тема проверки'">{{
        item["theme"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['results']" :label="'Результат'">{{
        item["results"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дата записи'">
        {{ new Date(item["created"]).toLocaleString("ru-RU") }}
      </ElementsLabelSlot>
      <template v-if="editable" #footer>
        <TabMenu
          :item="'poligrafs'"
          @cancel="modal = false"
          @update="
            poligraf = item;
            modal = true;
          "
          @delete="deletePoligraf(item['id'], index)"
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
