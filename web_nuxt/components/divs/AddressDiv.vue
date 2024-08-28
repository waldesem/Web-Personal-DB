<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Address } from "@/utils/interfaces";

const anketaState = stateAnketa();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const address = ref({} as Address); 

function cancelAction() {
  edit.value = false;
  collapse.value = false;
  itemId.value = "";
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
      <UCard>
        <FormsAddressForm @cancel="cancelAction" />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.addresses.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.addresses"
      :key="idx"
      class="py-3"
    >
      <UCard>
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
          <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'addresses')"
            @update="
              address = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </div>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Адреса отсутствуют</p>
  </div>
</template>

