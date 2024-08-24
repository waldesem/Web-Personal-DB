<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Relation } from "@/utils/interfaces";

const anketaState = stateAnketa();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const relation = ref({} as Relation);

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}

const editState = inject("editState") as boolean
</script>

<template>
  <UButton
    v-if="editState"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="p-1">
      <div class="border rounded p-3">
        <FormsRelationForm @cancel="cancelAction" />
      </div>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.relations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.relations"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
        <FormsRelationForm
          v-if="edit && itemId == item['id'].toString()"
          :relation="relation"
          @cancel="edit = !edit"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тип'">{{
            item["relation"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Связь'">
            <router-link
              :to="{
                name: 'profile',
                params: { id: item['relation_id'] },
              }"
            >
              ID #{{ item["relation_id"] }}
            </router-link>
          </ElementsLabelSlot>
          <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'relations')"
            @update="
              relation = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>

