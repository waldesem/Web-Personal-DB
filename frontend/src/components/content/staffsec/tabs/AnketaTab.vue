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
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
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
      <LabelValue :label="'Действия'">
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
      </LabelValue>
      <LabelValue :label="'ID'">{{ props.resume["id"] }}</LabelValue>
      <LabelValue :label="'Фамилия'">{{ props.resume["surname"] }}</LabelValue>
      <LabelValue :label="'Имя'">{{ props.resume["firstname"] }}</LabelValue>
      <LabelValue :label="'Отчество'">{{
        props.resume["patronymic"]
      }}</LabelValue>
      <LabelValue :label="'Предыдущая фамилия'"
        >{{ props.resume["previous"] }}
      </LabelValue>
      <LabelValue :label="'Дата рождения'"
        >{{
          new Date(String(props.resume["birthday"])).toLocaleDateString("ru-RU")
        }}
      </LabelValue>
      <LabelValue :label="'Место рождения'">{{
        props.resume["birthplace"]
      }}</LabelValue>
      <LabelValue :label="'Гражданство'">{{
        props.resume["country"]
      }}</LabelValue>
      <LabelValue :label="'Двойное гражданство'"
        >{{ props.resume["ext_country"] }}
      </LabelValue>
      <LabelValue :label="'СНИЛС'">{{ props.resume["snils"] }}</LabelValue>
      <LabelValue :label="'ИНН'">{{ props.resume["inn"] }}</LabelValue>
      <LabelValue :label="'Образование'"
        >{{ props.resume["education"] }}
      </LabelValue>
      <LabelValue :label="'Семейнное положение'"
        >{{ props.resume["marital"] }}
      </LabelValue>
      <LabelValue :label="'Дополнительная информация'"
        >{{ props.resume["addition"] }}
      </LabelValue>
      <LabelValue :label="'Статус'"
        >{{ storeClassify.classData.status[props.resume["status_id"]] }}
      </LabelValue>
      <LabelValue :label="'Дата создания'"
        >{{
          props.resume["created"]
            ? new Date(String(props.resume["created"])).toLocaleDateString(
                "ru-RU"
              )
            : ""
        }}
      </LabelValue>
      <LabelValue :label="'Дата обновления'"
        >{{
          props.resume["updated"]
            ? new Date(String(props.resume["updated"])).toLocaleDateString(
                "ru-RU"
              )
            : ""
        }}
      </LabelValue>
      <LabelValue :label="'Пользователь'">{{
        props.resume["user_id"]
      }}</LabelValue>
      <LabelValue :label="'Материалы'">
        <router-link
          v-if="props.resume['path']"
          :to="{
            name: 'manager',
            query: { path: props.resume['path'].split('/') },
          }"
        >
          {{ props.resume["path"] }}
        </router-link>
      </LabelValue>
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

    <div class="btn-group d-print-none mt-3" role="group">
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
          storeClassify.classData.status[props.resume['status_id']] !== 'Проверка'
          && props.resume.user_id !== props.userId && props.spinner
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
</template>
