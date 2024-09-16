<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Address } from "@/types/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean;

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const address = ref({} as Address);

const { refresh } = await useLazyAsyncData("addresses", async () => {
  await anketaState.getItem('addresses');
})

async function updateAddress(addressForm: Address) {
  closeAction();
  anketaState.updateItem("addresses", addressForm);
  refresh()
}

async function deleteAddress(index: string) {
  anketaState.deleteItem(index, 'addresses');
  refresh()
}

async function cancelOperation() {
  closeAction();
  refresh()
}

function closeAction() {
  edit.value = false;
  collapse.value = false;
  itemId.value = "";  
}
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
        <FormsAddressForm 
          @cancel="cancelOperation" 
          @submit="updateAddress"
        />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.addresses && anketaState.anketa.value.addresses.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.addresses"
      :key="idx"
      class="py-3"
    >
      <UCard>
        <FormsAddressForm
          v-if="edit && itemId == item['id'].toString()"
          :addrs="address"
          @cancel="cancelOperation"
          @submit="updateAddress"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тип'">{{
            item["view"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Адрес'">{{
            item["addresses"]
          }}</ElementsLabelSlot>
        </div>
        <template
          v-show="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :last-index="2"
            @delete="deleteAddress(item['id'])"
            @update="
              address = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Адреса отсутствуют</p>
  </div>
</template>
