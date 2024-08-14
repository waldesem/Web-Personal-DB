<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Previous } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const previous = ref({} as Previous);

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
    <FormsPreviousForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.previous.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.previous"
      :key="idx"
      class="border rounded p-3"
    >
      <FormsPreviousForm
        v-if="edit && itemId == item['id'].toString()"
        :previous="previous"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot :label="'Фамилия'">
          {{ item["surname"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Имя'">
          {{ item["firstname"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot v-if="item['patronymic']" :label="'Отчество'">
          {{ item["patronymic"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot v-if="item['changed']" :label="'Год изменения'">
          {{ item["changed"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot v-if="item['reason']" :label="'Причина'">
          {{ item["reason"] }}
        </ElementsLabelSlot>
        <ElementsNaviHorizontal
          v-show="
            anketaState.anketa.value.persons['user_id'] ==
              userState.user.value.userId &&
            anketaState.anketa.value.persons['standing']
          "
          :last-index="2"
          @delete="anketaState.deleteItem(item['id'].toString(), 'previous')"
          @update="
            previous = item;
            itemId = item['id'].toString();
            edit = true;
          "
        />
        <UDivider v-show="idx < anketaState.anketa.value.previous.length - 1" />
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные отсутствуют</p>
  </div>
</template>
