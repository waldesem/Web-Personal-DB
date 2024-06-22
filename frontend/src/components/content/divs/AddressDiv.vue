<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Address } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
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

onBeforeMount(async () => {
  await stateAnketa.getItem("addresses");
});

const address = ref({
  action: "",
  itemId: "",
  item: <Address>{},
  showActions: false,
});

function cancelAction(){
  address.value.action = "";
  address.value.itemId = "";
  address.value.item = <Address>({});
};

function submitForm(form: Object) {
  stateAnketa.updateItem(
    "addresses",
    form
  );
  cancelAction();
}
</script>

<template>
  <ActionHeader
    :id="'address'"
    :header="'Адреса'"
    :action="address.action"
    @action="address.action = address.action ? '' : 'create'"
  />
  <AddressForm
    v-if="address.action === 'create'"
    @submit="submitForm"
    @cancel="cancelAction()"
  />
  <div
    v-if="stateAnketa.anketa.addresses.length"
    class="collapse show"
    id="address"
  >
    <div
      v-for="(item, idx) in stateAnketa.anketa.addresses"
      :key="idx"
      @mouseover="address.showActions = true"
      @mouseout="address.showActions = false"
      class="card card-body mb-3"
    >
      <AddressForm
        v-if="
          address.action === 'update' &&
          address.itemId === item['id'].toString()
        "
        :addrs="address.item"
        @submit="submitForm"
        @cancel="cancelAction()"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="address.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'addresses')"
            @update="
              address.action = 'update';
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
