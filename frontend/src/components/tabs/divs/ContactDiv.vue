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
const ContactForm = defineAsyncComponent(
  () => import("@components/forms/ContactForm.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();


interface Contact {
  id: string;
  view: string;
  contact: string;
}

onBeforeMount(() => {
  contact.value.getItem();
});

const contact = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Contact>{},
  items: Array<Contact>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/contact/${candId}`
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
</script>

<template>
  <h6>
    Контакты
    <a
      class="btn btn-link"
      @click="
        contact.isForm = !contact.isForm;
        contact.action = contact.isForm ? 'create' : '';"
      :title="contact.isForm ? 'Закрыть форму' : 'Добавить информацию'"
    >
      <i
        :class="contact.isForm ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"
      ></i>
    </a>
  </h6>
  <template v-if="contact.isForm">
    <ContactForm 
      :get-item="contact.getItem"
      :action="contact.action"
      :cand-id="candId"
      :content="contact.item"
      @deactivate="contact.deactivateForm"
    />
  </template>
  <template v-else>
    <div v-if="contact.items.length > 0">
      <CollapseDiv
        v-for="(item, idx) in contact.items"
        :key="idx"
        :id="'cont' + idx"
        :idx="idx"
        :label="'Контакт #' + (idx + 1)"
      >
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              href="#"
              @click="contact.deleteItem(item['id'].toString())"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="
                contact.isForm = true;
                contact.action = 'update';
                contact.item = item;
                contact.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Вид'" :value="item['view']" />
        <RowDivSlot :label="'Контакт'" :value="item['contact']" />
      </CollapseDiv>
    </div>
    <p v-else>Данные отсутствуют</p>
  </template>
</template>
