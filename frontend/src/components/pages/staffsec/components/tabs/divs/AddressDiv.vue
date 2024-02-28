<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Address } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const AddressForm = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/forms/AddressForm.vue")
);

onBeforeMount( async() => {
  await props.getItem("staff");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Address[],
    default: () => ({}),
  },
  getItem: {
    type: Function,
    required: true,
  },
  updateItem: {
    type: Function,
    required: true,
  },
  deleteItem: {
    type: Function,
    required: true,
  },
});

const address = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Address>{},
});
</script>

<template>
  <h6>
    Адреса
    <a
      class="btn btn-link"
      @click="
        address.isForm = !address.isForm;
        address.action = address.isForm ? 'create' : '';
      "
      :title="address.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="address.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="address.isForm">
    <AddressForm
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :action="address.action"
      :cand-id="candId"
      :content="address.item"
      @deactivate="address.isForm = false; address.action = '';"
    />
  </template>
  <template v-else>
    <div v-if="props.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.items"
        :key="idx"
        :id="'addr' + idx"
        :idx="idx"
        :label="'Адрес #' + (idx + 1)"
      >
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="props.deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                address.action = 'update';
                address.isForm = true;
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
</template>
