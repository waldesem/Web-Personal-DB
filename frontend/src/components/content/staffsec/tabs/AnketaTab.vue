<script setup lang="ts">
import { ref, defineAsyncComponent, computed } from "vue";
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

const resumeObj = computed(() => {
  return {
    region: [
      "Регион",
      storeClassify.classData.regions[props.resume["region_id"]],
    ],
    surname: ["Фамилия", props.resume["surname"]],
    name: ["Имя", props.resume["firstname"]],
    patronymic: ["Отчество", props.resume["patronymic"]],
    previous_surname: ["Предыдущая фамилия", props.resume["previous"]],
    birthday: ["Дата рождения", props.resume["birthday"]],
    birthplace: ["Место рождения", props.resume["birthplace"]],
    country: ["Гражданство", props.resume["country"]],
    ext_country: ["Двойное гражданство", props.resume["ext_country"]],
    snils: ["СНИЛС", props.resume["snils"]],
    inn: ["ИНН", props.resume["inn"]],
    education: ["Образование", props.resume["education"]],
    marital: ["Семейнное положение", props.resume["marital"]],
    additional: ["Дополнительная информация", props.resume["addition"]],
    status: [
      "Статус",
      storeClassify.classData.status[props.resume["status_id"]],
    ],
    created: [
      "Дата создания",
      props.resume["created"]
        ? new Date(String(props.resume["created"])).toLocaleDateString("ru-RU")
        : "",
    ],
    updated: [
      "Дата обновления",
      props.resume["updated"]
        ? new Date(String(props.resume["updated"])).toLocaleDateString("ru-RU")
        : "",
    ],
    user_id: ["Пользователь", props.resume["user_id"]],
  };
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
}
</script>

<template>
  <div class="py-3">
    <ResumeForm
      v-if="dataResume.action"
      :action="dataResume.action"
      :resume="props.resume"
      @get-resume="getResume"
      @cancel="dataResume.action = ''"
    />
    <div v-else>
      <div class="row mb-3 d-print-none">
        <div class="col-md-3">
          <label class="form-label">Действия</label>
        </div>
        <div class="col-md-9">
          <a
            class="btn btn-link"
            title="Изменить"
            @click="dataResume.action = 'update'"
          >
            <i class="bi bi-pencil-square"></i>
          </a>
          <a
            class="btn btn-link"
            title="Удалить"
            :disabled="
              storeClassify.classData.status[props.resume['status_id']] ===
                'finish' || props.spinner
            "
            @click="deleteItem(props.resume['id'], 'resume')"
          >
            <i class="bi bi-trash"></i>
          </a>
        </div>
      </div>
      <div v-for="(value, key) in resumeObj" :key="key" class="row mb-3">
        <div class="col-md-3">
          <label class="form-label">
            {{ value[0] }}
          </label>
        </div>
        <div class="col-md-9">
          {{ value[1] }}
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-md-3">
          <label class="form-label">Материалы</label>
        </div>
        <div class="col-md-9">
          <router-link
            v-if="props.resume['path']"
            :to="{
              name: 'manager',
              query: { path: props.resume['path'].split('/') },
            }"
          >
            {{ props.resume["path"] }}
          </router-link>
        </div>
      </div>
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

    <div class="d-print-none row mb-3">
      <div class="offset-lg-2 col-lg-10">
        <div class="btn-group" role="group">
          <button
            :disabled="
              props.resume.user_id !== null && props.resume.user_id !== ''
            "
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
                  'repeat') ||
              props.resume.user_id === '' ||
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
        </div>
      </div>
    </div>
  </div>
</template>
