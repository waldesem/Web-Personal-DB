<script setup lang="ts">
import type { Relation } from "@/types/interfaces";

prefetchComponents(["FormsRelationForm", "ElementsSkeletonDiv"]);

const emit = defineEmits(["delete", "submit"]);

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
const edit = ref(false);
const itemId = ref("");
const relation = ref({} as Relation);
const relations = ref<Relation[]>([]);

const { refresh, status } = await useLazyAsyncData("relations", async () => {
  relations.value = await authFetch("/api/items/relations/" + props.candId) as Relation[];
});

async function submitRelation(form: Relation) {
  closeAction();
  pending.value = true;
  await emit("submit", form, "relations");
  pending.value = false;
  await refresh();
}

async function deleteRelation(id: string) {
  closeAction();
  await emit("delete", id, "relations");
  await refresh();
}

function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsRelationForm
          :cand-id="props.candId"
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
        <FormsRelationForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :relation="relation"
          @cancel="cancelOperation"
          @update="submitRelation"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тип'">{{
            item["relation"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Связь'">
            <NuxtLink :to="`/profile/${item['relation_id']}`">
              ID #{{ item["relation_id"] }}
            </NuxtLink>
          </ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="3"
            @delete="deleteRelation(item['id'].toString())"
            @update="
              relation = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @upgrade="refresh()"
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="2" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
