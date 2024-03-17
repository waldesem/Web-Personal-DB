<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Address } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
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

const addrObj = computed(() => {
  return props.items.map((item) => ({
    id: ["ID", item['id']],
    view: ["Тип", item['view']],
    region: ["Регион", item['region']],
    address: ["Адрес", item['address']],
  }));
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
    <div v-if="addrObj.length">
      <CollapseDiv
        v-for="(item, idx) in addrObj"
        :key="idx"
        :id="'addr' + idx"
        :idx="idx.toString()"
        :label="'Адрес #' + (idx + 1)"
      >
        <div class="row mb-3 d-print-none">
          <div class="col-md-3">
            <label class="form-label">Действия</label>
          </div>
          <div class="col-md-9">
            <a
              href="#"
              @click="emit('delete', item.id[1].toString(), 'address')"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                address.action = 'update';
                address.item = props.items[idx];
                address.itemId = item.id[1].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </div>
        </div>
        <LabelValue v-for="(value, key) in item" :key="key"
          :label="value[0]"
          :value="value[1]"
        />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
