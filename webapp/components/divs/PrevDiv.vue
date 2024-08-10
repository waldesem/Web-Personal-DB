<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Previous } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const collapse = ref(false);
const edit = ref(false);
const itemId = ref('');
const previous = ref(<Previous>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton label="Предыдущие" variant="link" @click="collapse = !collapse" />
  <div class="border rounded m-3">
    <FormsPreviousForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.previous.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.previous"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="border rounded m-3"
    >
      <FormsPreviousForm 
        v-if="edit && itemId == item['id'].toString()" 
        :previous="previous" 
        @cancel="cancelAction" 
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
                actions &&
                anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
                anketaState.anketa.value.persons['standing']
              "
            @delete="anketaState.deleteItem(item['id'].toString(), 'previous')"
            @update="
              previous = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
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
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
