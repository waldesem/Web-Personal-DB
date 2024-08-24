<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Address } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const address = ref({} as Address); 

function cancelAction() {
  edit.value = false;
  collapse.value = false;
  itemId.value = "";
}
</script>

<template>
  <UButton
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="p-1">
      <div class="border rounded p-3">
        <FormsAddressForm @cancel="cancelAction" />
      </div>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.addresses.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.addresses"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
        <FormsAddressForm
          v-if="edit && itemId == item['id'].toString()"
          :addrs="address"
          @cancel="cancelAction"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тип'">{{ item["view"] }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Адрес'">{{
            item["addresses"]
          }}</ElementsLabelSlot>
          <ElementsNaviHorizontal
            v-show="
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['editable']
            "
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'addresses')"
            @update="
              address = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Адреса отсутствуют</p>
  </div>
</template>

