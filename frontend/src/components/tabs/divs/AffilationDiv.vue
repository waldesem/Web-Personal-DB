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
const AffilationForm = defineAsyncComponent(
  () => import("@components/forms/AffilationForm.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();

interface Affilation {
  id: string;
  view: string;
  name: string;
  inn: string;
  position: string;
  deadline: string;
}

onBeforeMount(() => {
  affilation.value.getItem();
});

const affilation = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Affilation>{},
  items: Array<Affilation>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/affilation/${candId}`
      );
      this.items = response.data;
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Ошибка: ${error}`
      );
    }
  },

  deleteItem: async function (id: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/affilation/${id}`
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
    Аффилированность
    <a
      class="btn btn-link"
      @click="
        affilation.isForm = !affilation.isForm;
        affilation.action = affilation.isForm ? 'create' : '';"
      :title="affilation.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="affilation.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="affilation.isForm">
    <AffilationForm 
      :get-item="affilation.getItem"
      :action="affilation.action"
      :cand-id="candId"
      :content="affilation.item"
      @deactivate="affilation.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="affilation.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in affilation.items"
        :key="idx"
        :id="'affil' + idx"
        :idx="idx"
        :label="'Аффилированность #' + (idx + 1)"
      >
      <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="affilation.deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                affilation.isForm = true;
                affilation.action = 'update';
                affilation.item = item;
                affilation.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Тип участия'" :value="item['view']" />
        <RowDivSlot :label="'Организация'" :value="item['name']" />
        <RowDivSlot :label="'ИНН'" :value="item['inn']" />
        <RowDivSlot :label="'Должность'" :value="item['position']" />
        <RowDivSlot
          :label="'Дата декларации'"
          :value="new Date(item['deadline']).toLocaleDateString('ru-RU')"
        />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
