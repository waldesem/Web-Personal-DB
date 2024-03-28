<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { classifyStore } from "@/store/classify";
import type { Anketa, Resume } from "@/interfaces/interface";

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
  anketa: {
    type: Object as () => Anketa,
    default: {},
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
      :resume="props.anketa.resume"
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
            storeClassify.classData.status[props.anketa.resume['status_id']] ===
              'finish' || props.spinner
          "
          @click="deleteItem(props.anketa.resume['id'], 'resume')"
        >
          <i class="bi bi-trash"></i>
        </a>
      </LabelValue>
      <LabelValue :label="'ID'">{{ props.anketa.resume["id"] }}</LabelValue>
      <LabelValue :label="'Фамилия'">{{ props.anketa.resume["surname"] }}</LabelValue>
      <LabelValue :label="'Имя'">{{ props.anketa.resume["firstname"] }}</LabelValue>
      <LabelValue :label="'Отчество'">{{
        props.anketa.resume["patronymic"]
      }}</LabelValue>
      <LabelValue :label="'Предыдущая фамилия'"
        >{{ props.anketa.resume["previous"] }}
      </LabelValue>
      <LabelValue :label="'Дата рождения'"
        >{{
          new Date(String(props.anketa.resume["birthday"])).toLocaleDateString("ru-RU")
        }}
      </LabelValue>
      <LabelValue :label="'Место рождения'">{{
        props.anketa.resume["birthplace"]
      }}</LabelValue>
      <LabelValue :label="'Гражданство'">{{
        props.anketa.resume["country"]
      }}</LabelValue>
      <LabelValue :label="'Двойное гражданство'"
        >{{ props.anketa.resume["ext_country"] }}
      </LabelValue>
      <LabelValue :label="'СНИЛС'">{{ props.anketa.resume["snils"] }}</LabelValue>
      <LabelValue :label="'ИНН'">{{ props.anketa.resume["inn"] }}</LabelValue>
      <LabelValue :label="'Образование'"
        >{{ props.anketa.resume["education"] }}
      </LabelValue>
      <LabelValue :label="'Семейнное положение'"
        >{{ props.anketa.resume["marital"] }}
      </LabelValue>
      <LabelValue :label="'Дополнительная информация'"
        >{{ props.anketa.resume["addition"] }}
      </LabelValue>
      <LabelValue :label="'Статус'"
        >{{ storeClassify.classData.status[props.anketa.resume["status_id"]] }}
      </LabelValue>
      <LabelValue :label="'Дата создания'"
        >{{
          props.anketa.resume["created"]
            ? new Date(String(props.anketa.resume["created"])).toLocaleDateString(
                "ru-RU"
              )
            : ""
        }}
      </LabelValue>
      <LabelValue :label="'Дата обновления'"
        >{{
          props.anketa.resume["updated"]
            ? new Date(String(props.anketa.resume["updated"])).toLocaleDateString(
                "ru-RU"
              )
            : ""
        }}
      </LabelValue>
      <LabelValue :label="'Пользователь'">{{
        props.anketa.resume["user_id"]
      }}</LabelValue>
      <LabelValue :label="'Материалы'">
        <router-link
          v-if="props.anketa.resume['path']"
          :to="{
            name: 'manager',
            query: { path: props.anketa.resume['path'].split('/') },
          }"
        >
          {{ props.anketa.resume["path"] }}
        </router-link>
      </LabelValue>
    </div>

    <StaffDiv
      :items="props.anketa.staffs"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <DocumentDiv
      :items="props.anketa.documents"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <AddressDiv
      :items="props.anketa.addresses"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <ContactDiv
      :items="props.anketa.contacts"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <RelationDiv
      :items="props.anketa.relations"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <WorkplaceDiv
      :items="props.anketa.workplaces"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <AffilationDiv
      :items="props.anketa.affilations"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />

    <div class="btn-group d-print-none mt-3" role="group">
      <button
        :disabled="props.anketa.resume.user_id !== null && props.anketa.resume.user_id !== ''"
        type="button"
        class="btn btn-outline-primary"
        @click="getResume('self')"
      >
        Взять на проверку
      </button>

      <button
        class="btn btn-outline-primary"
        :disabled="
          storeClassify.classData.status[props.anketa.resume['status_id']] !== 'Проверка'
          && props.anketa.resume.user_id !== props.userId && props.spinner
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
