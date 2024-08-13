<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Needs } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const need = ref({} as Needs);

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
    <FormsInquiryForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.inquiries.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.inquiries"
      :key="idx"
      class="border rounded p-3"
    >
      <FormsInquiryForm
        v-if="edit && itemId == item['id'].toString()"
        :inquiry="need"
        @cancel="cancelAction"
      />
      <div v-else>
        <p class="text-primary">
          {{ "Запросы о сотруднике #" + (idx + 1) }}
        </p>
        <ElementsLabelSlot :label="'Информация'">{{
          item["info"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Иннициатор'">{{
          item["origins"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{
          item["username"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
        <ElementsNaviHorizontal
          v-show="
            !idx &&
            anketaState.anketa.value.persons['user_id'] ==
              userState.user.value.userId &&
            anketaState.anketa.value.persons['standing']
          "
          :last-index="2"
          @delete="anketaState.deleteItem(item['id'].toString(), 'inquiries')"
          @update="
            need = item;
            itemId = item['id'].toString();
            edit = true;
          "
        />
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Запросы о сотруднике не поступали</p>
  </div>
</template>
