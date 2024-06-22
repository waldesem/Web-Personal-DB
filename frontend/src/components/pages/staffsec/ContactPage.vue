<script setup lang="ts">
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
const ConnectForm = defineAsyncComponent(
  () => import("@components/content/forms/ConnectForm.vue")
);

onBeforeMount(async () => {
  await getContacts();
});

const contactData = ref({
  contacts: [],
  action: "",
  search: "",
  item: <Connection>{},
});

async function getContacts(): Promise<void> {
  contactData.value.action = "";
  contactData.value.item = <Connection>({});
  try {
    const response = await axiosAuth.get(
      `${server}/connects`,
      {
        params: {
          search: contactData.value.search,
        },
      }
    );
    contactData.value.contacts = response.data;
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
        `${server}/connects/${id}`
      );
      console.log(response.status);
      stateAlert.setAlert(
        "alert-success",
        `Контакт с ID ${id} удален`
      );
      getContacts();
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
  getContacts();
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
    :item="contactData.item"
    @get-contacts="getContacts()"
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
        <tr>
          <td colspan="7">
            <TableSlots
              id="overflow"
              :tbl-class="'table table-hover align-middle no-bottom-border'"
            >
              <template v-slot:tbody>
                <tr
                  v-for="contact in contactData.contacts"
                  :key="contact['id']"
                >
                  <td width="18%">{{ contact["company"] }}</td>
                  <td width="18%">
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
                  <td width="18%">{{ contact["phone"] }}</td>
                  <td width="18%">{{ contact["adding"] }}</td>
                  <td width="18%">{{ contact["mobile"] }}</td>
                  <td width="5%">
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
          </td>
        </tr>
      </template>
    </TableSlots>
  </div>
</template>

<style scoped>
#overflow {
  max-height: 50vh;
  overflow-y: auto;
}
.no-bottom-border td {
  border-bottom: none;
}
</style>