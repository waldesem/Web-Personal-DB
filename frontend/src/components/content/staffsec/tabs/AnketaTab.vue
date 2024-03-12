<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { classifyStore } from "@/store/classify";
import type {
  Resume,
  Staff,
  Document,
  Address,
  Contact,
  Relation,
  Work,
  Affilation,
} from "@/interfaces/interface";

const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("../forms/ResumeForm.vue")
);
const StaffDiv = defineAsyncComponent(() => import("../divs/StaffDiv.vue"));
const DocumentDiv = defineAsyncComponent(
  () => import("../divs/DocumentDiv.vue")
);
const AddressDiv = defineAsyncComponent(() => import("../divs/AddressDiv.vue"));
const ContactDiv = defineAsyncComponent(() => import("../divs/ContactDiv.vue"));
const RelationDiv = defineAsyncComponent(
  () => import("../divs/RelationDiv.vue")
);
const WorkplaceDiv = defineAsyncComponent(
  () => import("../divs/WorkplaceDiv.vue")
);
const AffilationDiv = defineAsyncComponent(
  () => import("../divs/AffilationDiv.vue")
);

const storeClassify = classifyStore();

const emit = defineEmits([
  "get-item",
  "get-resume",
  "delete",
  "submit",
  "file",
]);

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
  spinner: {
    type: Boolean,
    required: true,
  },
  resume: {
    type: Object as () => Resume,
    default: {},
  },
  staffs: {
    type: Array as () => Array<Staff>,
    default: () => [],
  },
  documents: {
    type: Array as () => Array<Document>,
    default: () => [],
  },
  addresses: {
    type: Array as () => Array<Address>,
    default: () => [],
  },
  contacts: {
    type: Array as () => Array<Contact>,
    default: () => [],
  },
  relations: {
    type: Array as () => Array<Relation>,
    default: () => [],
  },
  workplaces: {
    type: Array as () => Array<Work>,
    default: () => [],
  },
  affilations: {
    type: Array as () => Array<Affilation>,
    default: () => [],
  },
});

const dataResume = ref({
  action: "",
  form: <Resume>{},
});

function getResume(action: string) {
  emit("get-resume", action);
}

function getItem(item: string) {
  emit("get-item", item);
}

function updateItem(
  action: string,
  item: string,
  itemId: string,
  form: Object
) {
  emit("submit", action, item, itemId, form);
}

function deleteItem(itemId: string, item: string) {
  emit("delete", itemId, item);
};
</script>

<template>
  <div class="py-3">
    <ResumeForm v-if="dataResume.action"
      :action="dataResume.action"
      :resume="props.resume"
      @get-resume="getResume"
      @cancel="dataResume.action = ''"
    />
    <div v-else>
      <LabelSlot>
        <a
          class="btn btn-link"
          title="Изменить"
          @click="dataResume.action = 'update'"
        >
          <i class="bi bi-pencil-square"></i>
        </a>
      </LabelSlot>
      <LabelValue
        :label="'Регион'"
        :value="storeClassify.classData.regions[props.resume['region_id']]"
      />
      <LabelValue
        :label="'Фамилия'"
        :value="props.resume['surname']"
      />
      <LabelValue
        :label="'Имя'"
        :value="props.resume['firstname']"
      />
      <LabelValue
        :label="'Отчество'"
        :value="props.resume['patronymic']"
      />
      <LabelValue :label="'Изменение имени'" :value="props.resume['previous']" />
      <LabelValue :label="'Дата рождения'" :value="props.resume['birthday']" />
      <LabelValue :label="'Место рождения'" :value="props.resume['birthplace']" />
      <LabelValue :label="'Гражданство'" :value="props.resume['country']" />
      <LabelValue
        :label="'Второе гражданство'"
        :value="props.resume['ext_country']"
      />
      <LabelValue :label="'СНИЛС'" :value="props.resume['snils']" />
      <LabelValue :label="'ИНН'" :value="props.resume['inn']" />
      <LabelValue :label="'Образование'" :value="props.resume['education']" />
      <LabelValue :label="'Семейное положение'" :value="props.resume['marital']" />
      <LabelValue
        :label="'Дополнительная информация'"
        :value="props.resume['addition']"
      />
      <LabelSlot :label="'Материалы'">
        <router-link v-if="props.resume['path']"
          :to="{
            name: 'manager',
            query: { path: props.resume['path'].split('/') },
          }"
        >
          {{ props.resume["path"] }}
        </router-link>
      </LabelSlot>
      <LabelSlot :label="'Статус'">
        <a href="#" @click="getResume('status')">
          {{ storeClassify.classData.status[props.resume["status_id"]] }}
        </a>
      </LabelSlot>
      <LabelValue
        :label="'Создан'"
        :value="
          props.resume['created']
            ? new Date(String(props.resume['created'])).toLocaleDateString(
                'ru-RU'
              )
            : ''
        "
      />
      <LabelValue
        :label="'Обновлен'"
        :value="
          props.resume['updated']
            ? new Date(String(props.resume['updated'])).toLocaleDateString(
                'ru-RU'
              )
            : ''
        "
      />
      <LabelValue :label="'Внешний ID'" :value="props.resume['request_id']" />
    </div>

    <StaffDiv
      :items="props.staffs"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <DocumentDiv
      :items="props.documents"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <AddressDiv
      :items="props.addresses"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <ContactDiv
      :items="props.contacts"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <RelationDiv
      :items="props.relations"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <WorkplaceDiv
      :items="props.workplaces"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <AffilationDiv
      :items="props.affilations"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />

    <div class="d-print-none py-3">
      <BtnGroup :cls="false">
        <button
          :disabled="props.resume.user_id !== null && props.resume.user_id !== ''"
          type="button"
          class="btn btn-outline-primary"
          @click="getResume('self')"
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
                'repeat') || props.resume.user_id === '' ||
            props.resume.user_id !== props.userId ||
            props.spinner
          "
          @click="getResume('send')"
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
          @click="deleteItem(props.resume['id'], 'resume')"
        >
          Удалить анкету
        </button>
      </BtnGroup>
    </div>
  </div>
</template>
