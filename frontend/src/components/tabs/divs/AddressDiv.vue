<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref, inject } from "vue";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const AddressForm = defineAsyncComponent(
  () => import("@components/forms/AddressForm.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();

interface Address {
  id: string;
  view: string;
  region: string;
  address: string;
}

onBeforeMount(() => {
  address.value.getItem();
});

const address = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Address>{},
  items: Array<Address>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/address/${candId}`
      );
      this.items = response.data;
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert("alert-danger", `Ошибка: ${error}`);
    }
  },

  deleteItem: async function (id: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/address/${id}`
      );
      console.log(response.status);
      this.getItem();

      storeAlert.alertMessage.setAlert(
        "alert-info",
        `Запись с ID ${id} удалена`
      );
    } catch (error) {
      console.error(error);
    }
  },

  deactivateForm: function () {
    this.isForm = false;
    this.action = "";
  },
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
      :get-item="address.getItem"
      :action="address.action"
      :cand-id="candId"
      :content="address.item"
      @deactivate="address.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="address.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in address.items"
        :key="idx"
        :id="'addr' + idx"
        :idx="idx"
        :label="'Адрес #' + (idx + 1)"
      >
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="address.deleteItem(item['id'].toString())"
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
