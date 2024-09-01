<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Document } from "@/utils/interfaces";

const anketaState = stateAnketa();

const collapse = ref(false);
const itemId = ref("");
const edit = ref(false);
const doc = ref({} as Document);

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
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsDocumentForm @cancel="cancelAction" />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.documents.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.documents"
      :key="idx"
      class="p-1"
    >
      <UCard>
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
        </div>
        <template
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'documents')"
            @update="
              doc = item;
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

