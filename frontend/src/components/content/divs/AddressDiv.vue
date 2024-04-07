<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Address } from "@/interfaces/interface";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
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
  handleMouse() {
    this.showActions = !this.showActions;
  }
});

function submitForm(form: Object) {
  emit("submit", address.value.action, "address", address.value.itemId, form);
  address.value.action = "";
};
</script>

<template>
  <ActionHeader
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
    :class="{ 'border border-primary rounded': address.showActions }"
    @mouseover="address.handleMouse"
    @mouseout="address.handleMouse"
  >
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'addr' + idx"
        :label="'Адрес #' + (idx + 1)"
      >
        <LabelSlot v-show="address.showActions">
          <ActionIcons
            @delete="emit('delete', item['id'].toString(), 'address')"
            @update="
              address.action = 'update';
              address.item = item;
              address.itemId = item['id'].toString();
            "
          />
        </LabelSlot>
        <LabelSlot :label="'ID'">{{ item['id'] }}</LabelSlot>
        <LabelSlot :label="'Тип'">{{ item['view'] }}</LabelSlot>
        <LabelSlot :label="'Регион'">{{ item['region'] }}</LabelSlot>
        <LabelSlot :label="'Адрес'">{{ item['address'] }}</LabelSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
