<script setup lang="ts">
import type { Relation } from "@/types/interfaces";

prefetchComponents(["FormsRelationForm", "ElementsSkeletonDiv"]);

const emit = defineEmits(["message", "update"]);

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
  relations: {
    type: Array,
    default: () => [] as Relation[],
  },
});

const collapse = ref(false);
const pending = ref(false);
const itemId = ref("");
const relation = ref({} as Relation);

async function submitRelation(form: Relation) {
  closeAction();
  pending.value = true;
  const { message } = (await authFetch(`/api/relations/${props.candId}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  emit("update");
  emit("message", message);
}

async function deleteRelation(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/api/relations/${props.candId}/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  emit("update");
  emit("message", message);
}

function cancelOperation() {
  closeAction();
  emit("update");
}

function closeAction() {
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
  <div v-if="props.relations && props.relations.length">
    <div v-for="(item, idx) in props.relations" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="pending" :rows="2" />
      <ElementsCardDiv v-else>
        <ElementsLabelSlot :label="'Тип'">{{
          item["type"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Связь'">
          <NuxtLink :to="`/profile/${item['right_id']}`">
            ID #{{ item["right_id"] }}
          </NuxtLink>
        </ElementsLabelSlot>
        <template
          v-if="props.editable"
          #footer
        >
          <ElementsNaviHorizont
            :nav-items="2"
            @delete="deleteRelation(item['id'].toString())"
            @update="
              relation = item;
              itemId = item['id'].toString();
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
