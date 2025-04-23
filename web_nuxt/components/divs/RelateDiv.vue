<script setup lang="ts">
import type { Relation, Relationship } from "@/types";

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const relations = ref([] as Relation[]);
const relationships = ref([] as Relationship[]);

const { refresh, status } = await useLazyAsyncData("relations", async () => {
  [relations.value, relationships.value] = (await authFetch(
    "/route/items/relations/" + candId.value
  )) as [Relation[], Relationship[]];
});

async function submitRelation(form: Relation) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/relations/${candId.value}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  refresh();
  emitMessage(message);
}

async function deleteRelation(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(
    `/route/items/relations/${candId.value}/${id}`,
    {
      method: "DELETE",
    }
  )) as Record<string, string>;
  if (message == "success") {
    relations.value.splice(idx, 1);
  }
  emitMessage(message);
}
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
      variant="ghost"
      icon="i-heroicons-plus-circle"
      @click="modal = !modal"
    />
  </div>
  <UModal
    v-model:open="modal"
    :dismissible="false"
    title="Связи"
    description="Данные профиля"
  >
    <template #content>
      <ElementsCardDiv>
        <FormsRelationForm @cancel="modal = false" @update="submitRelation" />
      </ElementsCardDiv>
    </template>
  </UModal>
  <div v-for="(item, idx) in relations" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Тип'">{{ item.type }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Связан'">
        <NuxtLink :to="`/profile/${item.right_id}`">
          ID #{{ item.right_id }}
        </NuxtLink>
      </ElementsLabelSlot>
      <template v-if="editable" #footer>
        <UButton
          label="Удалить"
          variant="ghost"
          icon="i-heroicons-trash"
          @click="deleteRelation(item.right_id, idx)"
        />
      </template>
    </ElementsCardDiv>
  </div>

  <div v-for="(item, idx) in relationships" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Тип'">{{ item.type }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Явяляется связью'">
        <NuxtLink :to="`/profile/${item.left_id}`">
          ID #{{ item.left_id }}
        </NuxtLink>
      </ElementsLabelSlot>
    </ElementsCardDiv>
  </div>
</template>
