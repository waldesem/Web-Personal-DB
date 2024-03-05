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

function cancelEdit(){
  address.value.action = '';
  address.value.item = {};
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
        address.action = address.action ? '' : 'create';
      "
      :title="address.action ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="address.action ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="address.action">
    <AddressForm
      :content="address.item"
      @submit="submitForm"
      @cancel="cancelEdit"
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
