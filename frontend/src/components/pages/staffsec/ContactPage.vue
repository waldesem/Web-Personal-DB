<script setup lang="ts">
import { onBeforeMount, defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@/store/alert";
import { debounce, server } from "@utilities/utils";
import { Connection } from "@/interfaces/interface";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/elements/TableSlots.vue")
);
const PageSwitcher = defineAsyncComponent(
  () => import("@components/layouts/PageSwitcher.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);
const ConnectForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/ConnectForm.vue")
);

const storeAuth = authStore();
const storeAlert = alertStore();

onBeforeMount(async () => {
  await getContacts(1);
});

const searchContacts = debounce(() => {
  getContacts(1);
}, 500);

const contactData = ref({
  names: [],
  companies: [],
  cities: [],
  contacts: [],
  page: 1,
  prev: false,
  next: false,
  action: "",
  search: "",
  item: <Connection>{},
});

async function getContacts(page: number): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.get(
      `${server}/connect/${page}`,
      {
        params: {
          search: contactData.value.search,
        },
      }
    );
    const [datas, has_prev, has_next, names, companies, cities] = response.data;
    Object.assign(contactData.value, {
      contacts: datas,
      names: names.names,
      companies: companies.companies,
      cities: cities.cities,
      prev: has_prev.has_prev,
      next: has_next.has_next,
    });
  } catch (error) {
    console.error(error);
  }
};

async function deleteContact(id: string): Promise<void> {
  if (confirm("Вы действительно хотите удалить контакт?")) {
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/connect/${id}`
      );
      console.log(response.status);
      storeAlert.alertMessage.setAlert(
        "alert-success",
        `Контакт с ID ${id} удален`
      );
      getContacts(contactData.value.page);
    } catch (error) {
      console.log(error);
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Ошибка при удалении контакта с ID ${id}`
      );
    }
  }
};
</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Контакты'" />
    <form @input.prevent="searchContacts" class="form form-check" role="form">
      <InputLabel
        :lbl-cls="'visually-hidden'"
        :cls-input="'col-lg-12'"
        :lbl="'Поиск'"
        :name="'search'"
        :placeholder="'Поиск по организации, имени, номеру мобильного телефона'"
        v-model="contactData.search"
      />
    </form>
    <ModalWin
      :id="'modalConnect'"
      :title="
        contactData.action === 'create'
          ? 'Добавить контакт'
          : 'Обновить контакт'
      "
      :size="'modal-lg'"
      @cancel="contactData.action = ''"
    >
      <ConnectForm
        :page="contactData.page"
        :action="contactData.action"
        :names="contactData.names"
        :companies="contactData.companies"
        :cities="contactData.cities"
        :item="contactData.item"
        @get-contacts="getContacts"
      />
    </ModalWin>
    <TableSlots :tbl-caption="'Список контактов'">
      <template v-slot:thead>
        <tr>
          <th width="4%">#</th>
          <th width="10%">Компания</th>
          <th width="10%">Название</th>
          <th width="10%">Город</th>
          <th width="10%">Имя</th>
          <th width="10%">Телефон</th>
          <th width="5%">Добавочный</th>
          <th width="10%">Мобильный</th>
          <th width="10%">E-mail</th>
          <th width="10%">Примечание</th>
          <th width="5%">Дата</th>
          <th width="3%">
            <a
              type="button"
              data-bs-toggle="modal"
              data-bs-target="#modalConnect"
              @click="contactData.action = 'create'"
              title="Добавить контакт"
            >
              <i class="bi bi-plus-circle"></i>
            </a>
          </th>
          <th width="3%"></th>
        </tr>
      </template>
      <template v-slot:tbody v-if="contactData.contacts.length > 0">
        <tr
          v-for="contact in contactData.contacts"
          :key="contact['id']"
          class="table align-middle text-center"
        >
          <td>{{ contact["id"] }}</td>
          <td>{{ contact["name"] }}</td>
          <td>{{ contact["company"] }}</td>
          <td>{{ contact["city"] }}</td>
          <td>{{ contact["fullname"] }}</td>
          <td>{{ contact["phone"] }}</td>
          <td>{{ contact["adding"] }}</td>
          <td>{{ contact["mobile"] }}</td>
          <td>{{ contact["mail"] }}</td>
          <td>{{ contact["comment"] }}</td>
          <td>{{ contact["data"] }}</td>
          <td>
            <a
              class="btn btn-link"
              type="button"
              data-bs-toggle="modal"
              data-bs-target="#modalConnect"
              title="Изменить контакт"
              @click="
                contactData.action = 'edit';
                contactData.item = contact;
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </td>
          <td width="5%">
            <a
              href="#"
              title="Удалить"
              @click="deleteContact(contact['id'])"
            >
              <i class="bi bi-trash"></i>
            </a>
          </td>
        </tr>
      </template>
    </TableSlots>
    <PageSwitcher
      :has_prev="contactData.next"
      :has_next="contactData.prev"
      :switchPrev="contactData.page - 1"
      :switchNext="contactData.page + 1"
      @switch="getContacts"
    />
  </div>
</template>

