<script setup lang="ts">
import type { Relation, Relationship } from "@/types";

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const relations = ref([] as Relation[]);
const relationships = ref([] as Relationship[]);
const index = ref(0);

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
  pending.value = false;
  index.value = 0;
  if (message == "success") {
    relations.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <UCard
    class="m-2"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <USwitch
      v-if="editable"
      v-model="edit"
      :label="edit ? 'Отключить редактирование' : 'Включить редактирование'"
      size="xs"
      class="mb-2 me-2 justify-end"
    />
    <div v-for="(item, idx) in relationships" :key="idx" class="p-1">
      <UCard>
        <ElementsLabelSlot :label="'Тип'">{{ item.type }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Явяляется связью'">
          <NuxtLink :to="`/profile/${item.left_id}`">
            ID #{{ item.left_id }}
          </NuxtLink>
        </ElementsLabelSlot>
      </UCard>
    </div>

    <div v-for="(item, idx) in relations" :key="idx" class="p-1">
      <UCard>
        <div class="flex">
          <div v-if="edit" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="staff" :value="idx">
          </div>
          <div class="flex-grow">
            <ElementsLabelSlot :label="'Тип'">{{
              item.type
            }}</ElementsLabelSlot>
            <ElementsLabelSlot :label="'Связан'">
              <NuxtLink :to="`/profile/${item.right_id}`">
                ID #{{ item.right_id }}
              </NuxtLink>
            </ElementsLabelSlot>
          </div>
        </div>
      </UCard>
    </div>
    <template v-if="edit" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Связи"
        description="Данные профиля"
      >
        <template #content>
          <UCard>
            <FormsRelationForm
              @cancel="modal = false"
              @update="submitRelation"
            />
          </UCard>
        </template>
      </UModal>
      <UButton
        label="Добавить запись"
        variant="ghost"
        icon="i-heroicons-plus-circle"
        @click="modal = !modal"
      />
      <UButton
        label="Удалить"
        variant="ghost"
        icon="i-heroicons-trash"
        @click="deleteRelation(relations[index].right_id, index)"
      />
    </template>
  </UCard>
</template>
