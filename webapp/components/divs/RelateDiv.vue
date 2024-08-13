<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Relation } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const relation = ref({} as Relation);

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <div v-if="collapse" class="border rounded p-3">
    <FormsRelationForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.relations.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.relations"
      :key="idx"
      class="border rounded p-3"
    >
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
        <ElementsNaviHorizontal
          v-show="
            anketaState.anketa.value.persons['user_id'] ==
              userState.user.value.userId &&
            anketaState.anketa.value.persons['standing']
          "
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
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>
