<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Address } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const address = ref(<Address>{});

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
  <div v-if="collapse" class="border rounded p-3">
    <FormsAddressForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.addresses.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.addresses"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="border rounded p-3"
    >
      <FormsAddressForm
        v-if="edit && itemId == item['id'].toString()"
        :addrs="address"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
              actions &&
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']
            "
            @delete="anketaState.deleteItem(item['id'].toString(), 'addresses')"
            @update="
              address = item;
              itemId = item['id'].toString();
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Тип'">{{ item["view"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Адрес'">{{
          item["addresses"]
        }}</ElementsLabelSlot>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Адреса отсутствуют</p>
  </div>
</template>
