<script setup lang="ts">
import { onBeforeMount, defineAsyncComponent, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@/store/alert";
import { debounce, server } from "@utilities/utils";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const ConnectForm = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/forms/ConnectForm.vue")
);
const PageSwitcher = defineAsyncComponent(
  () => import("@components/layouts/PageSwitcher.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

const storeAuth = authStore();
const storeAlert = alertStore();

onBeforeMount(async () => {
  await contactData.value.getContacts(1);
});

const searchContacts = debounce(() => {
  contactData.value.getContacts(1);
}, 500);

const contactData = ref({
  contacts: [],
  companies: [],
  cities: [],
  page: 1,
  prev: false,
  next: false,
  id: "",
  action: "",
  search: "",
  item: <Record<string, any>>{},

  getContacts: async function (page: number): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/connect/${page}`,
        {
          params: {
            search: this.search,
          },
        }
      );
      const [datas, has_prev, has_next, companies, cities] = response.data;
      Object.assign(this, {
        contacts: datas,
        companies: companies.companies,
        cities: cities.cities,
        prev: has_prev.has_prev,
        next: has_next.has_next,
      });
    } catch (error) {
      console.error(error);
    }
  },

  deleteContact: async function (id: string): Promise<void> {
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
        this.getContacts(this.page);
      } catch (error) {
        console.log(error);
        storeAlert.alertMessage.setAlert(
          "alert-danger",
          `Ошибка при удалении контакта с ID ${id}`
        );
      }
    }
  },
});
</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Контакты'" />
    <form @input.prevent="searchContacts" class="form form-check" role="form">
      <div class="row py-3">
        <input
          class="form-control"
          id="search"
          name="search"
          type="search"
          placeholder="Поиск по организации, имени, номеру мобильного телефона"
          v-model="contactData.search"
        />
      </div>
    </form>
    <div v-if="contactData.action">
      <ModalWin
        :id="'modalConnect'"
        :title="
          contactData.action === 'create'
            ? 'Добавить контакт'
            : 'Обновить контакт'
        "
        :size="'modal-sm'"
        @deactivate="contactData.action = ''"
      >
        <ConnectForm
          :id="contactData.id"
          :page="contactData.page"
          :action="contactData.action"
          :companies="contactData.companies"
          :cities="contactData.cities"
          :item="contactData.item"
          :getContacts="contactData.getContacts"
          @deactivate="contactData.action = ''"
        />
      </ModalWin>
    </div>
    <div class="py-3">
      <table class="table align-middle text-center no-bottom-border">
        <thead>
          <tr>
            <th width="5%">#</th>
            <th width="10%">Компания</th>
            <th width="10%">Город</th>
            <th width="10%">Имя</th>
            <th width="10%">Телефон</th>
            <th width="10%">Добавочный</th>
            <th width="10%">Мобильный</th>
            <th width="10%">E-mail</th>
            <th width="10%">Примечание</th>
            <th width="5%">Дата</th>
            <th width="5%">
              <a
                role="button"
                type="button"
                data-bs-toogle="modal"
                data-bs-target="#modalConnect"
                @click="contactData.action === 'create'"
                title="Добавить контакт"
              >
                <i class="bi bi-plus-circle"></i>
              </a>
            </th>
            <th width="5%"></th>
          </tr>
        </thead>
        <tbody v-if="contactData.contacts.length > 0">
          <tr>
            <td colspan="12">
              <table
                v-for="contact in contactData.contacts"
                :key="contact['id']"
                class="table align-middle text-center"
              >
                <tbody>
                  <tr v-if="contactData.id !== contact['id']">
                    <td width="5%">{{ contact["id"] }}</td>
                    <td width="10%">{{ contact["company"] }}</td>
                    <td width="10%">{{ contact["city"] }}</td>
                    <td width="10%">{{ contact["fullname"] }}</td>
                    <td width="10%">{{ contact["phone"] }}</td>
                    <td width="10%">{{ contact["adding"] }}</td>
                    <td width="10%">{{ contact["mobile"] }}</td>
                    <td width="10%">{{ contact["mail"] }}</td>
                    <td width="10%">{{ contact["comment"] }}</td>
                    <td width="5%">{{ contact["data"] }}</td>
                    <td width="5%">
                      <a
                        class="btn btn-link"
                        type="button"
                        data-bs-toogle="modal"
                        data-bs-target="#modalConnect"
                        title="Изменить контакт"
                        @click="
                          contactData.action = 'edit';
                          contactData.id = contact['id'];
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
                        @click="contactData.deleteContact(contact['id'])"
                      >
                        <i class="bi bi-trash"></i>
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <PageSwitcher
      :has_prev="contactData.next"
      :has_next="contactData.prev"
      :switchPrev="contactData.page - 1"
      :switchNext="contactData.page + 1"
      :switchPage="contactData.getContacts"
    />
  </div>
</template>

<style scoped>
.no-bottom-border td {
  border-bottom: none;
}
</style>
@/store/auth