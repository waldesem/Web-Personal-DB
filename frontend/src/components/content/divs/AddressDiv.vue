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

function submitForm(form: Object) {
  stateAnketa.updateItem(
    address.value.action,
    "addresses",
    address.value.itemId,
    form
  );
  Object.keys(form).forEach((key) => {
    delete form[key as keyof typeof form];
  })
  address.value.action = "";
  address.value.itemId = "";
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
    @cancel="
      address.action = '';
      address.itemId = '';
    "
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
        @cancel="
          address.action = '';
          address.itemId = '';
        "
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
          />
        </LabelSlot>
        <LabelSlot :label="'Тип'">{{ item["view"] }}</LabelSlot>
        <LabelSlot :label="'Адрес'">{{ item["address"] }}</LabelSlot>
        <LabelSlot :label="'Дата'">
          {{ new Date(String(item["created"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot v-if="item['updated']" :label="'Обновлено'">
          {{ new Date(String(item["updated"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
