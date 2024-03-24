<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Address } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/CollapseDiv.vue")
);
const AddressForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/AddressForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
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
        <LabelValue :label="'Действия'" :no-print="true">
          <a
            href="#"
            @click="emit('delete', item['id'].toString(), 'address')"
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            @click="
              address.action = 'update';
              address.item = item;
              address.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </LabelValue>
        <LabelValue :label="'ID'">{{ item['id'] }}</LabelValue>
        <LabelValue :label="'Тип'">{{ item['view'] }}</LabelValue>
        <LabelValue :label="'Регион'">{{ item['region'] }}</LabelValue>
        <LabelValue :label="'Адрес'">{{ item['address'] }}</LabelValue>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
