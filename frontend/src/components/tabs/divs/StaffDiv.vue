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
const StaffForm = defineAsyncComponent(
  () => import("@components/forms/StaffForm.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();

interface Staff {
  id: string;
  position: string;
  department: string;
}

onBeforeMount(() => {
  staff.value.getItem();
});

const staff = ref({
  action: "",
  itemId: "",
  item: <Staff>{},
  staffs: Array<Staff>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/staff/${candId}`
      );
      this.staffs = response.data;
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
    this.action = "";
  },
});
</script>

<template>
  <h6>
    Должности
    <a
      class="btn btn-link"
      @click="staff.action = 'create'"
      :title="staff.action !== '' ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="staff.action !== '' ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="staff.action !== ''">
    <StaffForm
      :get-item="staff.getItem"
      :action="staff.action"
      :cand-id="candId"
      :content="staff.item"
      @deactivate="staff.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="staff.staffs.length > 0">
      <CollapseDiv
        v-for="(item, idx) in staff.staffs"
        :key="idx"
        :id="'staff' + idx"
        :idx="idx"
        :label="'Должность #' + (idx + 1)"
      >
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="staff.deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                staff.action = 'update';
                staff.item = item;
                staff.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Должность'" :value="item['position']" />
        <RowDivSlot :label="'Департамент'" :value="item['department']" />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
@/utilities/token