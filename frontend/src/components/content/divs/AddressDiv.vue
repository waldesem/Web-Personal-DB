<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Address } from "@/interfaces/interface";

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
  emit("get-item", "address");
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
});

function submitForm(form: Object) {
  emit("submit", address.value.action, "address", address.value.itemId, form);
  address.value.action = "";
};
</script>

<template>
  <h6>
    Адреса
    <a
      class="btn btn-link"
      title="Добавить информацию"
      @click="address.action = 'create'"
    >
    <i
        :class="address.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <AddressForm v-if="address.action"
    :addrs="address.item"
    @submit="submitForm"
  />
  <div v-else>
    <div v-if="props.items.length">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'addr' + idx"
        :idx="idx.toString()"
        :label="'Адрес #' + (idx + 1)"
      >
        <LabelSlot :label="'Действия'" :no-print="true">
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
