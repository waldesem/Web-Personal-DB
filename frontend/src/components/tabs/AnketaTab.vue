<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { classifyStore } from "@/store/classify";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";
import { 
  Resume, 
  Staff, 
  Document,
  Address,
  Contact,
  Relation,
  Work,
  Affilation,
} from "@/interfaces/interface";

const ResumeForm = defineAsyncComponent(
  () => import("@components/forms/ResumeForm.vue")
);
const StaffDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/StaffDiv.vue")
);
const DocumentDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/DocumentDiv.vue")
);
const AddressDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/AddressDiv.vue")
);
const ContactDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/ContactDiv.vue")
);
const RelationDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/RelationDiv.vue")
);
const WorkplaceDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/WorkplaceDiv.vue")
);
const AffilationDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/AffilationDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const storeClassify = classifyStore();
const storeAuth = authStore();
const storeAlert = alertStore();

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  resume: {
    type: Object as () => Resume,
    default: () => {},
  },
  spinner: Boolean,
  getResume: {
    type: Function,
    required: true,
  },
  deleteResume: {
    type: Function,
    required: true,
  },
});

const dataResume = ref({
  action: "",
  item: "",
  form: <Record<string, any>>{},

  deactivateForm: function () {
    this.action = "";
    this.item = "";
  },
});

const briefData = ref({
  staffs: <Array<Staff>>[],
  documents: <Array<Document>>[],
  addresses: <Array<Address>>[],
  contacts: <Array<Contact>>[],
  relations: <Array<Relation>>[],
  workplaces: <Array<Work>>[],
  affilations: <Array<Affilation>>[],

  getItem: async function (param: string): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/${param}/${props.candId}`
      );
      switch (param) {
        case "staff":
          this.staffs = response.data;
          break;
        case "document":
          this.documents = response.data;
          break;
        case "address":
          this.addresses = response.data;
          break;
        case "contact":
          this.contacts = response.data;
          break;
        case "relation":
          this.relations = response.data;
          break;
        case "workplace":
          this.workplaces = response.data;
          break;
        case "affilation":
          this.affilations = response.data;
          break;
        default:
          break;
      }
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Ошибка: ${error}`
      );
    }
  },

  deleteItem: async function (id: string, param: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/staff/${id}`
      );
      console.log(response.status);
      this.getItem(param);

      storeAlert.alertMessage.setAlert(
        "alert-info",
        `Запись с ID ${id} удалена`
      );
    } catch (error) {
      console.error(error);
    }
  },
})
</script>

<template>
  <div class="py-3">
    <template v-if="dataResume.item === 'resume'">
      <ResumeForm
        :get-item="props.getResume"
        :action="dataResume.action"
        :cand-id="candId"
        :content="props.resume"
        @deactivate="dataResume.deactivateForm"
      />
    </template>

    <template v-else>
      <div v-if="props.resume">
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="dataResume.item = 'update'"
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot
          :label="'Категория'"
          :value="
            storeClassify.classData.category[props.resume['category_id']]
          "
        />
        <RowDivSlot
          :label="'Регион'"
          :value="
            storeClassify.classData.regions[props.resume['region_id']]
          "
        />
        <RowDivSlot
          :label="'Фамилия Имя Отчество'"
          :value="props.resume['fullname']"
        />
        <RowDivSlot
          :label="'Изменение имени'"
          :value="props.resume['previous']"
        />
        <RowDivSlot
          :label="'Дата рождения'"
          :value="props.resume['birthday']"
        />
        <RowDivSlot
          :label="'Место рождения'"
          :value="props.resume['birthplace']"
        />
        <RowDivSlot
          :label="'Гражданство'"
          :value="props.resume['country']"
        />
        <RowDivSlot
          :label="'Второе гражданство'"
          :value="props.resume['ext_country']"
        />
        <RowDivSlot :label="'СНИЛС'" :value="props.resume['snils']" />
        <RowDivSlot :label="'ИНН'" :value="props.resume['inn']" />
        <RowDivSlot
          :label="'Образование'"
          :value="props.resume['education']"
        />
        <RowDivSlot
          :label="'Дополнительная информация'"
          :value="props.resume['addition']"
        />
        <RowDivSlot :label="'Материалы'" :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <router-link
              :to="{
                name: 'manager',
                params: { group: 'staffsec' },
                query: { path: props.resume['path'].split('/') },
              }"
            >
              {{ props.resume["path"] }}
            </router-link>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Статус'" :slotTwo="true">
          <template v-slot:divTwo>
            <a href="#" @click="props.getResume('status')">
              {{
                storeClassify.classData.status[props.resume["status_id"]]
              }}
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot
          :label="'Создан'"
          :value="
            new Date(String(props.resume['created'])).toLocaleDateString(
              'ru-RU'
            )
          "
        />
        <RowDivSlot
          :label="'Обновлен'"
          :value="
            new Date(String(props.resume['updated'])).toLocaleDateString(
              'ru-RU'
            )
          "
        />
        <RowDivSlot
          :label="'Внешний ID'"
          :value="props.resume['request_id']"
        />
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <StaffDiv 
      :cand-id="props.candId"
      :items="briefData.staffs"
      :get-item="briefData.getItem"
      :delete-item="briefData.deleteItem"
    />
    <DocumentDiv 
      :cand-id="props.candId"
      :items="briefData.documents"
      :get-item="briefData.getItem"
      :delete-item="briefData.deleteItem"
    />
    <AddressDiv 
      :cand-id="props.candId"
      :items="briefData.addresses"
      :get-item="briefData.getItem"
      :delete-item="briefData.deleteItem"
    />
    <ContactDiv 
      :cand-id="props.candId"
      :items="briefData.contacts"
      :get-item="briefData.getItem"
      :delete-item="briefData.deleteItem"
    />
    <RelationDiv 
      :cand-id="props.candId"
      :items="briefData.relations"
      :get-item="briefData.getItem"
      :delete-item="briefData.deleteItem"
    />
    <WorkplaceDiv 
      :cand-id="props.candId"
      :items="briefData.workplaces"
      :get-item="briefData.getItem"
      :delete-item="briefData.deleteItem"
    />
    <AffilationDiv 
      :cand-id="props.candId"
      :items="briefData.affilations"
      :get-item="briefData.getItem"
      :delete-item="briefData.deleteItem"
    />

    <div class="d-print-none py-3">
      <BtnGroupForm>
        <button 
          :disabled="props.resume.user_id !== ''"
          type="button"
          class="btn btn-outline-primary" 
          @click="props.getResume('self')">
          Взять на проверку
        </button>
        <button
          class="btn btn-outline-primary"
          :disabled="
            (storeClassify.classData.status[props.resume['status_id']] !==
              'new' &&
              storeClassify.classData.status[props.resume['status_id']] !==
                'update' &&
              storeClassify.classData.status[props.resume['status_id']] !==
                'repeat') ||
                props.spinner
          "
          @click="props.getResume('send')"
        >
          {{ !props.spinner ? "Отправить на проверку" : "" }}
          <span
            v-if="props.spinner"
            class="spinner-border spinner-border-sm"
          ></span>
          <span v-if="props.spinner" role="status">Отправляется...</span>
        </button>
        <button
          type="button"
          class="btn btn-outline-danger"
          :disabled="
            storeClassify.classData.status[props.resume['status_id']] ===
              'finish' || props.spinner
          "
          @click="props.deleteResume("resume")"
        >
          Удалить анкету
        </button>
      </BtnGroupForm>
    </div>
  </div>
</template>
