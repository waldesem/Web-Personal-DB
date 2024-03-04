<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const AddressForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/AddressForm.vue")
);

const emit = defineEmits(["get", "delete", "submit"]);

onBeforeMount(() => {
  emit("get", "address");
});

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  items: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const address = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Record<any, string>>{},
});

function deactivateEmit() {
  address.value.isForm = false; 
  address.value.action = '';
};

function submitForm(
  itemId: string, 
  form: Object
  ) {
  emit("submit", [address.value.action, "address", itemId, form])
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "address"])
};
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
      :action="address.action"
      :cand-id="candId"
      :content="address.item"
      @submit="submitForm"
      @deactivate="deactivateEmit"
    />
  </template>
  <template v-else>
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
