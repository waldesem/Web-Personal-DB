<script setup lang="ts">
import { onBeforeMount, defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@/store/alert";
import { debounce, server } from "@/utilities";
import { Connection } from "@/interfaces";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/content/elements/ModalWin.vue")
)
const ConnectDiv = defineAsyncComponent(
  () => import("@components/content/divs/ConnectDiv.vue")
)
const PageSwitcher = defineAsyncComponent(
  () => import("@components/content/elements/PageSwitcher.vue")
);
const ConnectForm = defineAsyncComponent(
  () => import("@components/content/forms/ConnectForm.vue")
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
  contactData.value.action = "";
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
  <div class="row mb-5">
    <HeaderDiv 
      :page-header="contactData.action 
        ? 'Изменить/добавить контакт' 
        : 'Контакты'" 
    />
  </div>
  <div v-show="contactData.action" class="mb-5">
    <ConnectForm
      :page="contactData.page"
      :action="contactData.action"
      :names="contactData.names"
      :companies="contactData.companies"
      :cities="contactData.cities"
      :item="contactData.item"
      @get-contacts="getContacts"
      @cancel-edit="contactData.action = ''"
    />
  </div>
  <div v-show="!contactData.action" class="mb-5">
    <input
      @input.prevent="searchContacts"
      class="form-control mb-5"
      name="search"
      id="search"
      type="text"
      placeholder="Поиск по организации, имени, номеру мобильного телефона"
      v-model="contactData.search"
    />
    <ModalWin
      :id="'modalConnect'"
      :title="contactData.item.fullname"
      :size="'modal-md'">
      <ConnectDiv :item="contactData.item"/>
    </ModalWin>
    <TableSlots>
      <template v-slot:caption>{{ `Список контактов` }}</template>
      <template v-slot:thead>
        <tr>
          <th width="18%">Название</th>
          <th width="18%">Имя</th>
          <th width="18%">Телефон</th>
          <th width="18%">Добавочный</th>
          <th width="18%">Мобильный</th>
          <th width="5%"></th>
          <th width="5%"></th>
        </tr>
      </template>
      <template v-slot:tbody v-if="contactData.contacts.length > 0">
        <tr
          v-for="contact in contactData.contacts"
          :key="contact['id']"
        >
          <td>{{ contact["company"] }}</td>
          <td>
            <a 
              href="#" 
              title="Посмотреть контакт"
              data-bs-target="#modalConnect" 
              data-bs-toggle="modal"
              @click="contactData.item = contact"
            >
              {{ contact["fullname"] }}
            </a>
          </td>
          <td>{{ contact["phone"] }}</td>
          <td>{{ contact["adding"] }}</td>
          <td>{{ contact["mobile"] }}</td>
          <td>
            <a
              class="btn btn-link"
              type="button"
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
    <a
      class="link link-primary d-flex justify-content-end"
      href="#"
      @click="contactData.action = 'create'"
      >
      Добавить контакт
    </a>
    <PageSwitcher
      :has_prev="contactData.next"
      :has_next="contactData.prev"
      :switchPrev="contactData.page - 1"
      :switchNext="contactData.page + 1"
      @switch="getContacts"
    />
  </div>
</template>

