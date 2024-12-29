<script setup lang="ts">
import type { Relation, Relationship } from "@/types";

prefetchComponents("FormsRelationForm");

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

const collapse = ref(false);
const pending = ref(false);
const itemId = ref("");
const relations = ref([] as Relation[]);
const relationships = ref([] as Relationship[]);

const { refresh, status } = await useLazyAsyncData("relations", async () => {
  [relations.value, relationships.value] = (await authFetch(
    "/route/items/relations/" + props.candId
  )) as [Relation[], Relationship[]];
});

async function submitRelation(form: Relation) {
  closeAction();
  pending.value = true;
  const { message } = (await authFetch(`/route/items/relations/${props.candId}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  refresh();
  emit("message", message);
}

async function deleteRelation(id: string, idx: integer) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/relations/${props.candId}/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    relationships.value.splice(idx, 1);
  };
  emit("message", message);
}

function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :disabled="status == 'pending' || pending"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsRelationForm
          @cancel="cancelOperation"
          @update="submitRelation"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="relations && relations.length">
    <div v-for="(item, idx) in relations" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="2" />
      <ElementsCardDiv v-else>
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
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="2" />
  </div>

  <div v-if="relationships && relationships.length">
    <div v-for="(item, idx) in relationships" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="2" />
      <ElementsCardDiv v-else>
        <ElementsLabelSlot :label="'Тип'">{{ item["type"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Явяляется связью'">
          <NuxtLink :to="`/profile/${item['left_id']}`">
            ID #{{ item["left_id"] }}
          </NuxtLink>
        </ElementsLabelSlot>
      </ElementsCardDiv>
    </div>
  </div>
  <p v-if="!relations && !relationships" class="text-primary">
    Данные отсутствуют
  </p>
</template>
