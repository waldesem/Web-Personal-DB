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
const DocumentForm = defineAsyncComponent(
  () => import("@components/forms/DocumentForm.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();

interface Document {
  id: string;
  view: string;
  series: string;
  number: string;
  agency: string;
  issue: string;
}


onBeforeMount(() => {
  document.value.getItem();
});

const document = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Document>{},
  items: Array<Document>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/document/${candId}`
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
        `${server}/document/${id}`
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
    Документы
    <a
      class="btn btn-link"
      @click="
        document.isForm = !document.isForm;
        document.action = document.isForm ? 'create' : '';"
      :title="document.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="document.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="document.isForm">
    <DocumentForm 
      :get-item="document.getItem"
      :action="document.action"
      :cand-id="candId"
      :content="document.item"
      @deactivate="document.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="document.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in document.items"
        :key="idx"
        :id="'docum' + idx"
        :idx="idx"
        :label="'Документ #' + (idx + 1)"
      >
      <RowDivSlot :slotTwo="true" :print="true">
        <template v-slot:divTwo>
          <a
            href="#"
            @click="
              document.deleteItem(item['id'].toString())"
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            class="btn btn-link"
            title="Изменить"
            @click="
              document.isForm = true;
              document.action = 'update';
              document.item = item;
              document.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </template>
      </RowDivSlot>
      <RowDivSlot :label="'Вид документа'" :value="item['view']" />
      <RowDivSlot :label="'Серия'" :value="item['series']" />
      <RowDivSlot :label="'Номер'" :value="item['number']" />
      <RowDivSlot :label="'Кем выдан'" :value="item['agency']" />
      <RowDivSlot
        :label="'Дата выдачи'"
        :value="new Date(String(item['issue'])).toLocaleDateString('ru-RU')"
      />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
