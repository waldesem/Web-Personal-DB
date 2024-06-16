<script setup lang="ts">
import  axios from "axios";
import { onBeforeMount, defineAsyncComponent, ref } from "vue";
import { axiosAuth } from "@/auth";
import { stateAlert } from "@/state";
import { debounce, server } from "@/utilities";
import { Connection } from "@/interfaces";
import { router } from "@/router";

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

onBeforeMount(async () => {
  await getConnects();
  await getContacts(1);
});

const contactData = ref({
  view: [],
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

async function getConnects(): Promise<void> {
  try {
    const response = await axios.get(`${server}/connects`);
    const { view, companies, cities } = response.data;
    Object.assign(contactData.value, {
      view: view,
      companies: companies,
      cities: cities,
    });
  } catch (error) {
    console.error(error);
  }
};

async function getContacts(page: number): Promise<void> {
  contactData.value.action = "";
  try {
    const response = await axiosAuth.get(
      `${server}/connect/${page}`,
      {
        params: {
          search: contactData.value.search,
        },
      }
    );
    const { contacts, has_prev, has_next} = response.data;
    Object.assign(contactData.value, {
      contacts: contacts,
      prev: has_prev,
      next: has_next,
    });
  } catch (error: any) {
    if (error.request.status == 401 || error.request.status == 403) {
      router.push({ name: "login" });
    } else {
      console.error(error);
    }
  }
};

async function deleteContact(id: string): Promise<void> {
  if (confirm("Вы действительно хотите удалить контакт?")) {
    try {
      const response = await axiosAuth.delete(
        `${server}/connect/${id}`
      );
      console.log(response.status);
      stateAlert.setAlert(
        "alert-success",
        `Контакт с ID ${id} удален`
      );
      getContacts(contactData.value.page);
    } catch (error) {
      console.log(error);
      stateAlert.setAlert(
        "alert-danger",
        `Ошибка при удалении контакта с ID ${id}`
      );
    }
  }
};

const searchContacts = debounce(() => {
  getContacts(1);
}, 500);
</script>

<template>
  <HeaderDiv 
    :page-header="contactData.action 
      ? 'Изменить/добавить контакт' 
      : 'Контакты'" 
  />
  <ConnectForm
    v-if="contactData.action" 
    :page="contactData.page"
    :action="contactData.action"
    :names="contactData.view"
    :companies="contactData.companies"
    :cities="contactData.cities"
    :item="contactData.item"
    @get-contacts="getContacts"
    @cancel-edit="contactData.action = ''"
  />
  <div v-show="!contactData.action" class="mb-3">
    <input
      @input.prevent="searchContacts"
      class="form-control mb-5"
      name="search"
      id="search"
      type="text"
      placeholder="Поиск по организации"
      v-model="contactData.search"
    />
    <ModalWin
      :id="'modalConnect'"
      :title="contactData.item.fullname"
      :size="'modal-md'">
      <ConnectDiv :item="contactData.item"/>
    </ModalWin>
    <TableSlots
      :class="{ 'table-hover': contactData.contacts.length > 0 }"
    >
      <template v-slot:caption>
        <button
          class="btn btn-link btn-sm"
          role="button"
          @click="contactData.action = 'create'"
        >
          Добавить контакт
        </button>  
      </template>
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
            <button
              class="btn btn-link"
              type="button"
              title="Изменить контакт"
              @click="
                contactData.action = 'edit';
                contactData.item = contact;
              "
            >
              <i class="bi bi-pencil-square"></i>
            </button>
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

