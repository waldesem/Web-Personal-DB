<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Relation } from "@/types/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean;

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const relation = ref({} as Relation);

const { refresh } = await useLazyAsyncData("relations", async () => {
  await anketaState.getItem('relations');
})

async function updateRelation(relationForm: Relation) {
  closeAction();  anketaState.updateItem("relations", relationForm);
  refresh()
}

async function deleteRelation(index: string) {
  anketaState.deleteItem(index, 'relations');
  refresh()
}

async function cancelOperation() {
  closeAction();
  refresh()
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="editState"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsRelationForm 
          @cancel="cancelOperation" 
          @submit="updateRelation"
        />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.relations && anketaState.anketa.value.relations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.relations"
      :key="idx"
      class="p-1"
    >
      <UCard>
        <FormsRelationForm
          v-if="edit && itemId == item['id'].toString()"
          :relation="relation"
          @cancel="cancelOperation"
          @submit="updateRelation"
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
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
        <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
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
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>
