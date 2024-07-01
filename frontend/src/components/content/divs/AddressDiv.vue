<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa } from "@/state";
import { Address } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const AddressForm = defineAsyncComponent(
  () => import("@components/content/forms/AddressForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const address = ref({
  itemId: "",
  item: <Address>{},
  showActions: false,
});

function cancelAction(){
  address.value.itemId = "";
  Object.keys(address.value.item).forEach(
    (key) => delete address.value.item[key as keyof typeof address.value.item]
  );
  const collapseAddress = document.getElementById('address');
  collapseAddress?.setAttribute('class', 'collapse card card-body');
};
</script>

<template>
  <DropDownHead :id="'address'" :header="'Адреса'"/>
  <div class="collapse card card-body" id="address">
    <AddressForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.addresses.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.addresses"
      :key="idx"
      @mouseover="address.showActions = true"
      @mouseout="address.showActions = false"
      class="card card-body mb-3"
    >
      <AddressForm
        v-if="address.itemId === item['id'].toString()"
        :addrs="address.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="address.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'addresses')"
            @update="
              address.item = item;
              address.itemId = item['id'].toString();
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Тип'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Адрес'">{{ item["address"] }}</LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>