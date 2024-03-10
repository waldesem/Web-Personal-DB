<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Address } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const AddressForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/AddressForm.vue")
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
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'addr' + idx"
        :idx="idx.toString()"
        :label="'Адрес #' + (idx + 1)"
      >
        <LabelSlot>
          <a
            href="#"
            @click="emit('delete', ['id'].toString(), 'address')"
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            data-bs-toggle="modal"
            data-bs-target="#modalAddress"
            @click="
              address.action = 'update';
              address.item = item;
              address.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </LabelSlot>>
        <LabelValue :label="'Тип'" :value="item['view']" />
        <LabelValue :label="'Регион'" :value="item['region']" />
        <LabelValue :label="'Адрес'" :value="item['address']" />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
