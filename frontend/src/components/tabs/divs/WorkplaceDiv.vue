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
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/forms/WorkplaceForm.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();


interface Work {
  id: string;
  start_date: string;
  end_date: string;
  workplace: string;
  address: string;
  reason: string;
  position: string;
}

onBeforeMount(() => {
  workplace.value.getItem();
});

const workplace = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Work>{},
  items: Array<Work>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/workplace/${candId}`
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
        `${server}/staff/${id}`
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
    Работа
    <a
      class="btn btn-link"
      @click="
        workplace.isForm = !workplace.isForm;  
        workplace.action = 'create'"
      :title="workplace.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="workplace.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="workplace.isForm">
    <WorkplaceForm 
      :get-item="workplace.getItem"
      :action="workplace.action"
      :cand-id="candId"
      :content="workplace.item"
      @deactivate="workplace.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="workplace.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in workplace.items"
        :key="idx"
        :id="'work' + idx"
        :idx="idx"
        :label="'Работа #' + (idx + 1)"
      >
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="workplace.deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                workplace.isForm = true;
                workplace.action = 'update';
                workplace.item = item;
                workplace.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Начало работы'" :value="item['start_date']" />
        <RowDivSlot :label="'Окончание работы'" :value="item['end_date']" />
        <RowDivSlot :label="'Организация'" :value="item['workplace']" />
        <RowDivSlot :label="'КоАдреснтакт'" :value="item['address']" />
        <RowDivSlot :label="'Должность'" :value="item['position']" />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
  
</template>
