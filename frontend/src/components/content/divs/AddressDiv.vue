<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
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

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item");
});

const props = defineProps({
  printPage: {
    type: Boolean,
    default: false,
  },
  items: {
    type: Array as () => Array<Address>,
    default: {},
  },
});

const address = ref({
  action: "",
  itemId: "",
  item: <Address>{},
  showActions: false,
});

function submitForm(form: Object) {
  emit("submit", address.value.action, "address", address.value.itemId, form);
  address.value.action = "";
};
</script>

<template>
  <ActionHeader
    :print-page="props.printPage"
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
      v-if="props.items.length" 
      :class="{'collapse show': !printPage}" 
      id="address"
    > 
      <div class="mb-3" v-for="(item, idx) in props.items" :key="idx">
        <div :class="{'card card-body': !printPage}">
          <LabelSlot>
            <ActionIcons v-show="address.showActions"
              @delete="emit('delete', item['id'].toString(), 'address')"
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
