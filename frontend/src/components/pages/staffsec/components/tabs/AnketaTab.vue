<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { classifyStore } from "@/store/classify";
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
  () => import("@components/pages/staffsec/components/forms/ResumeForm.vue")
);
const StaffDiv = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/divs/StaffDiv.vue")
);
const DocumentDiv = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/divs/DocumentDiv.vue")
);
const AddressDiv = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/divs/AddressDiv.vue")
);
const ContactDiv = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/divs/ContactDiv.vue")
);
const RelationDiv = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/divs/RelationDiv.vue")
);
const WorkplaceDiv = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/divs/WorkplaceDiv.vue")
);
const AffilationDiv = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/divs/AffilationDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const storeClassify = classifyStore();

const props = defineProps({
  candId: {
    type: String,
    required: true,
  },
  spinner: {
    type: Boolean,
    required: true,
  },
  resume: {
    type: () => <Resume>{},
    default: () => <Resume>{},
    },
  staffs: {
    type: () => <Array<Staff>>[],
    default: () => <Array<Staff>>[],
    },
  documents: {
    type: () => <Array<Document>>[],
    default: () => <Array<Document>>[],
  },
  addresses: {
    type: () => <Array<Address>>[],
    default: () => <Array<Address>>[],
  },
  contacts: {
    type: () => <Array<Contact>>[],
    default: () => <Array<Contact>>[],
  },
  relations: {
    type: () => <Array<Relation>>[],
    default: () => <Array<Relation>>[],
  },
  workplaces: {
    type: () => <Array<Work>>[],
    default: () => <Array<Work>>[],
  },
  affilations: {
    type: () => <Array<Affilation>>[],
    default: () => <Array<Affilation>>[],
  },
  getResume: {
    type: Function,
    required: true,
  },
  getItem: {
    type: Function,
    required: true,
  },
  updateItem: {
    type: Function,
    required: true,
  },
  deleteItem: {
    type: Function,
    required: true,
  },
});

onBeforeMount( async() => {
  await props.getItem("resume");
});

const dataResume = ref({
  action: "",
  item: "",
  form: <Resume>{},
});
</script>

<template>
  <div class="py-3">
    <template v-if="dataResume.item === 'resume'">
      <ResumeForm
        :get-item="props.getResume"
        :action="dataResume.action"
        :cand-id="props.candId"
        :content="props.resume"
        @deactivate="
          dataResume.action = '';
          dataResume.item = '';
        "
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
          :value="storeClassify.classData.category[props.resume['category_id']]"
        />
        <RowDivSlot
          :label="'Регион'"
          :value="storeClassify.classData.regions[props.resume['region_id']]"
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
        <RowDivSlot :label="'Гражданство'" :value="props.resume['country']" />
        <RowDivSlot
          :label="'Второе гражданство'"
          :value="props.resume['ext_country']"
        />
        <RowDivSlot :label="'СНИЛС'" :value="props.resume['snils']" />
        <RowDivSlot :label="'ИНН'" :value="props.resume['inn']" />
        <RowDivSlot :label="'Образование'" :value="props.resume['education']" />
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
              {{ storeClassify.classData.status[props.resume["status_id"]] }}
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
        <RowDivSlot :label="'Внешний ID'" :value="props.resume['request_id']" />
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <StaffDiv
      :cand-id="props.candId"
      :items="props.staffs"
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :delete-item="props.deleteItem"
    />
    <DocumentDiv
      :cand-id="props.candId"
      :items="props.documents"
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :delete-item="props.deleteItem"
    />
    <AddressDiv
      :cand-id="props.candId"
      :items="props.addresses"
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :delete-item="props.deleteItem"
    />
    <ContactDiv
      :cand-id="props.candId"
      :items="props.contacts"
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :delete-item="props.deleteItem"
    />
    <RelationDiv
      :cand-id="props.candId"
      :items="props.relations"
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :delete-item="props.deleteItem"
    />
    <WorkplaceDiv
      :cand-id="props.candId"
      :items="props.workplaces"
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :delete-item="props.deleteItem"
    />
    <AffilationDiv
      :cand-id="props.candId"
      :items="props.affilations"
      :get-item="props.getItem"
      :update-item="props.updateItem"
      :delete-item="props.deleteItem"
    />

    <div class="d-print-none py-3">
      <BtnGroupForm>
        <button
          :disabled="props.resume.user_id !== ''"
          type="button"
          class="btn btn-outline-primary"
          @click="props.getResume('self')"
        >
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
          @click="props.deleteItem('resume')"
        >
          Удалить анкету
        </button>
      </BtnGroupForm>
    </div>
  </div>
</template>
