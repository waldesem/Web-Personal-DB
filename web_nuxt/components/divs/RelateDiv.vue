<script setup lang="ts">
import type { Relation } from "@/types/interfaces";

const toast = useToast();

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
const edit = ref(false);
const itemId = ref("");
const relation = ref({} as Relation);

const {
  data: relations,
  refresh,
  status,
} = await useLazyAsyncData("relations", async () => {
  const response = await authFetch("/api/relations/" + props.candId);
  return response;
});

async function deleteRelation(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const response = await authFetch("/api/relations/" + id, {
    method: "DELETE",
  });
  console.log(response);
  toast.add({
    icon: "i-heroicons-information-circle",
    title: "Информация",
    description: `Запись с ID ${id} удалена`,
    color: "primary",
  });
  refresh();
}

async function cancelOperation() {
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
      <UCard>
        <FormsRelationForm @cancel="cancelOperation" @update="refresh" />
      </UCard>
    </div>
  </Transition>
  <div v-if="relations && relations.length">
    <div v-for="(item, idx) in relations" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending'" :rows="2" />
      <UCard v-else>
        <FormsRelationForm
          v-if="edit && itemId == item['id'].toString()"
          :relation="relation"
          @cancel="cancelOperation"
          @update="refresh"
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
            :navlen="2"
            @delete="deleteRelation(item['id'].toString())"
            @update="
              relation = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending'" :rows="2" />
    <p v-else class="text-primary">Данные отсутствуют</p>
  </div>
</template>
