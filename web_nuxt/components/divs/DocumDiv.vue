<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Document } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const itemId = ref("");
const edit = ref(false);
const doc = ref({} as Document);

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
  <div v-if="collapse" class="p-1">
    <div class="border rounded p-3">
      <FormsDocumentForm @cancel="cancelAction" />
    </div>
  </div>
  <div v-if="anketaState.anketa.value.documents.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.documents"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
        <FormsDocumentForm
          v-if="edit && itemId == item['id'].toString()"
          :docs="doc"
          @cancel="cancelAction"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Вид документа'">{{
            item["view"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Номер документа'">{{
            item["digits"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Серия документа'">{{
            item["series"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата выдачи'">
            {{
              item["issue"]
                ? new Date(String(item["issue"])).toLocaleDateString("ru-RU")
                : ""
            }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Кем выдан'">{{
            item["agency"]
          }}</ElementsLabelSlot>
          <ElementsNaviHorizontal
            v-show="
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['editable']
            "
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'documents')"
            @update="
              doc = item;
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
