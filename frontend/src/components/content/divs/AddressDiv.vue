<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Address } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const AddressForm = defineAsyncComponent(
  () => import("@components/content/forms/AddressForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(async() => {
  await stateAnketa.getItem("address");
});

const address = ref({
  action: "",
  itemId: "",
  item: <Address>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(address.value.action, "address", address.value.itemId, form);
  address.value.action = "";
};
</script>

<template>
  <ActionHeader
    :id="'address'"
    :header="'Адреса'"
    :action="address.action"
    @action="address.action = address.action ? '' : 'create'"
  />
  <AddressForm v-if="address.action"
    :addrs="address.item"
    @submit="submitForm"
    @cancel="address.action = ''"
  />
  <div v-else
    @mouseover="address.showActions = true"
    @mouseout="address.showActions = false"
  >
    <div 
      v-if="stateAnketa.anketa.address.length" 
      :class="{'collapse show': !stateAnketa.share.printPage}" 
      id="address"
    > 
      <div class="mb-3" v-for="(item, idx) in stateAnketa.anketa.address" :key="idx">
        <div :class="{'card card-body': !stateAnketa.share.printPage}">
          <LabelSlot>
            <ActionIcons v-show="address.showActions"
              @delete="stateAnketa.deleteItem(item['id'].toString(), 'address')"
              @update="
                address.action = 'update';
                address.item = item;
                address.itemId = item['id'].toString();
              "
            />
          </LabelSlot>
          <LabelSlot :label="'Тип'">{{ item['view'] }}</LabelSlot>
          <LabelSlot :label="'Регион'">{{ item['region'] }}</LabelSlot>
          <LabelSlot :label="'Адрес'">{{ item['address'] }}</LabelSlot>
        </div>
      </div>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
