<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref, inject } from "vue";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();

interface Robot {
  id: string;
  employee: string;
  document: string;
  inn: string;
  debt: string;
  bankruptcy: string;
  bki: string;
  courts: string;
  affiliation: string;
  terrorist: string;
  mvd: string;
  deadline: string;
}

onBeforeMount(() => {
  robot.value.getItem();
});

const robot = ref({
  items: Array<Robot>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/robot/${candId}`
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
        `${server}/robot/${id}`
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
});
</script>

<template>
  <div v-if="robot.items.length">
    <CollapseDiv
      v-for="(item, idx) in robot.items"
      :key="idx"
      :id="'check' + idx"
      :idx="idx"
      :label="'Робот #' + (idx + 1)"
    >
      <RowDivSlot
        :label="'Проверка по кадровым данным<'"
        :value="item['employee']"
      />
      <RowDivSlot :label="'Проверка ИНН'" :value="item['inn']" />
      <RowDivSlot :label="'Проверка ФССП'" :value="item['debt']" />
      <RowDivSlot
        :label="'Проверка банкротства'"
        :value="item['bankruptcy']"
      />
      <RowDivSlot :label="'Проверка БКИ'" :value="item['bki']" />
      <RowDivSlot :label="'Проверка судебных дел'" :value="item['courts']" />
      <RowDivSlot
        :label="'Проверка по списку террористов'"
        :value="item['terrorist']"
      />
      <RowDivSlot
        :label="'Проверка нахождения в розыске'"
        :value="item['mvd']"
      />
      <RowDivSlot
        :label="'Дата'"
        :value="new Date(String(item['deadline'])).toLocaleDateString('ru-RU')"
      />
    </CollapseDiv>
  </div>
</template>
