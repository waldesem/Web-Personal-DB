<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
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
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const address = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
});

function cancelEdit() {
  address.value.action = "";
  address.value.item = {};
}

function submitForm(form: Object) {
  emit("submit", [address.value.action, "address", address.value.itemId, form]);
  cancelEdit();
}

function deleteItem(itemId: string) {
  emit("delete", [itemId, "address"]);
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
      <i class="bi bi-plus-circle"></i>
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
      :id="'addr' + idx.toString()"
      :idx="idx.toString()"
      :label="'Адрес #' + (idx + 1).toString()"
    >
      <RowDivSlot :slotTwo="true" :print="true">
        <template v-slot:divTwo>
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
        </template>
      </RowDivSlot>
      <RowDivSlot :label="'Тип'" :value="item['view']" />
      <RowDivSlot :label="'Регион'" :value="item['region']" />
      <RowDivSlot :label="'Адрес'" :value="item['address']" />
    </CollapseDiv>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
