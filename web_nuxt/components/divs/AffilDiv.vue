<script setup lang="ts">
import type { Affilation } from "@/types";
import { emitMessage } from "@/utils";

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const affilation = ref({} as Affilation);
const affilations = ref<Affilation[]>([]);

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
  if (message == "success") {
    affilations.value.splice(idx, 1);
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
      <FormsAffilationForm
        :affil="affilation"
        @cancel="
          affilation = {} as Affilation;
          modal = false;
        "
        @update="submitAffilation"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in affilations" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Тип участия'">{{
        item["view"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Организация'">{{
        item["organization"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'ИНН'">{{ item["inn"] }}</ElementsLabelSlot>
      <template v-if="editable" #footer>
        <DivMenu
          @delete="deleteAffilation(item['id'], idx)"
          @update="
            affilation = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
