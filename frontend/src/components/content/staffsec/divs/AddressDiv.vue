<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Address } from "@/interfaces/interface";

const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);
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

function cancelEdit() {
  address.value.action = "";
  address.value.item = <Address>{};
}

function submitForm(form: Object) {
  emit("submit", address.value.action, "address", address.value.itemId, form);
  cancelEdit();
}

function deleteItem(itemId: string) {
  emit("delete", itemId, "address");
}
</script>

<template>
  <h6>
    Адреса
    <a
      class="btn btn-link"
      title="Добавить информацию"
      data-bs-toggle="modal"
      data-bs-target="#modalAddress"
      @click="address.action = 'create'"
    >
    <i
        :class="address.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <ModalWin
    :title="
      address.action === 'update' ? 'Изменить запись' : 'Добавить запись'
    "
    :id="'modalAddress'"
    @cancel="cancelEdit"
  >
    <AddressForm
      :content="address.item"
      @submit="submitForm"
    />
  </ModalWin>
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
          @click="deleteItem(item['id'].toString())"
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
</template>
