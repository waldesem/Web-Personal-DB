<script setup lang="ts">
import type { Relation, Relationship } from "@/types";

const emit = defineEmits(["message"]);

const authFetch = useFetchAuth();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const modal = ref(false);
const pending = ref(false);
const relations = ref([] as Relation[]);
const relationships = ref([] as Relationship[]);

const { refresh, status } = await useLazyAsyncData("relations", async () => {
  [relations.value, relationships.value] = (await authFetch(
    "/route/items/relations/" + props.candId
  )) as [Relation[], Relationship[]];
});

async function submitRelation(form: Relation) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(
    `/route/items/relations/${props.candId}`,
    {
      method: "POST",
      body: form,
    }
  )) as Record<string, string>;
  pending.value = false;
  refresh();
  emit("message", message);
}

async function deleteRelation(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(
    `/route/items/relations/${props.candId}/${id}`,
    {
      method: "DELETE",
    }
  )) as Record<string, string>;
  if (message == "success") {
    relations.value.splice(idx, 1);
  }
  emit("message", message);
}
</script>

<template>
  <UButton
    v-if="props.editable"
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
      <FormsRelationForm @cancel="modal = false" @update="submitRelation" />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in relations" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Тип'">{{ item["type"] }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Связан'">
        <NuxtLink :to="`/profile/${item['right_id']}`">
          ID #{{ item["right_id"] }}
        </NuxtLink>
      </ElementsLabelSlot>
      <template v-if="props.editable" #footer>
        <ElementsNavSimpHoriz
          :is-changed="false"
          @delete="deleteRelation(item['right_id'], idx)"
        />
      </template>
    </ElementsCardDiv>
  </div>

  <div v-for="(item, idx) in relationships" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Тип'">{{ item["type"] }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Явяляется связью'">
        <NuxtLink :to="`/profile/${item['left_id']}`">
          ID #{{ item["left_id"] }}
        </NuxtLink>
      </ElementsLabelSlot>
    </ElementsCardDiv>
  </div>
</template>
