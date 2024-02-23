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
const RelationForm = defineAsyncComponent(
  () => import("@components/forms/RelationForm.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();

interface Relation {
  id: string;
  relation: string;
  relation_id: string;
}

onBeforeMount(() => {
  relation.value.getItem();
});

const relation = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Relation>{},
  items: Array<Relation>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/relation/${candId}`
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
        `${server}/relation/${id}`
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
    Связи
    <a
      class="btn btn-link"
      @click="
        relation.isForm = !relation.isForm;
        relation.action = relation.isForm ? 'create' : '';"
      :title="relation.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="relation.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="relation.isForm">
    <RelationForm
      :get-item="relation.getItem"
      :action="relation.action"
      :cand-id="candId"
      :content="relation.item"
      @deactivate="relation.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="relation.items.length">
      <CollapseDiv
        v-for="(item, idx) in relation.items"
        :key="idx"
        :id="'relate' + idx"
        :idx="idx"
        :label="'Связь #' + (idx + 1)"
      >
      <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="relation.deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                relation.isForm = true;
                relation.action = 'update';
                relation.item = item;
                relation.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Тип связи'" :value="item['relation']" />
        <RowDivSlot :label="'Связь'" :slotTwo="true">
          <router-link
            :to="{
              name: 'profile',
              params: { group: 'staffsec', id: String(item['relation_id']) },
            }"
          >
            ID #{{ item["relation_id"] }}
          </router-link>
        </RowDivSlot>
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
