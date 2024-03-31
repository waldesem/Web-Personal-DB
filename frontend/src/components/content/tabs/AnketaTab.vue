<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { classifyStore } from "@/store/classify";
import type { Anketa, Resume } from "@/interfaces/interface";

const ResumeForm = defineAsyncComponent(
  () => import("@components/content/forms/ResumeForm.vue")
);
const StaffDiv = defineAsyncComponent(
  () => import("@components/content/divs/StaffDiv.vue")
);
const DocumentDiv = defineAsyncComponent(
  () => import("@components/content/divs/DocumentDiv.vue")
);
const AddressDiv = defineAsyncComponent(
  () => import("@components/content/divs/AddressDiv.vue")
);
const ContactDiv = defineAsyncComponent(
  () => import("@components/content/divs/ContactDiv.vue")
);
const RelationDiv = defineAsyncComponent(
  () => import("@components/content/divs/RelationDiv.vue")
);
const WorkplaceDiv = defineAsyncComponent(
  () => import("@components/content/divs/WorkplaceDiv.vue")
);
const AffilationDiv = defineAsyncComponent(
  () => import("@components/content/divs/AffilationDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
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
      <LabelSlot :label="'Действия'">
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
      </LabelSlot>
      <LabelSlot :label="'ID'">{{ props.anketa.resume["id"] }}</LabelSlot>
      <LabelSlot :label="'Фамилия'">{{
        props.anketa.resume["surname"]
      }}</LabelSlot>
      <LabelSlot :label="'Имя'">{{
        props.anketa.resume["firstname"]
      }}</LabelSlot>
      <LabelSlot :label="'Отчество'">{{
        props.anketa.resume["patronymic"]
      }}</LabelSlot>
      <LabelSlot :label="'Предыдущая фамилия'"
        >{{ props.anketa.resume["previous"] }}
      </LabelSlot>
      <LabelSlot :label="'Дата рождения'"
        >{{
          new Date(String(props.anketa.resume["birthday"])).toLocaleDateString(
            "ru-RU"
          )
        }}
      </LabelSlot>
      <LabelSlot :label="'Место рождения'">{{
        props.anketa.resume["birthplace"]
      }}</LabelSlot>
      <LabelSlot :label="'Гражданство'">{{
        props.anketa.resume["country"]
      }}</LabelSlot>
      <LabelSlot :label="'Двойное гражданство'"
        >{{ props.anketa.resume["ext_country"] }}
      </LabelSlot>
      <LabelSlot :label="'СНИЛС'">{{
        props.anketa.resume["snils"]
      }}</LabelSlot>
      <LabelSlot :label="'ИНН'">{{ props.anketa.resume["inn"] }}</LabelSlot>
      <LabelSlot :label="'Образование'"
        >{{ props.anketa.resume["education"] }}
      </LabelSlot>
      <LabelSlot :label="'Семейнное положение'"
        >{{ props.anketa.resume["marital"] }}
      </LabelSlot>
      <LabelSlot :label="'Дополнительная информация'"
        >{{ props.anketa.resume["addition"] }}
      </LabelSlot>
      <LabelSlot :label="'Статус'"
        >{{ storeClassify.classData.status[props.anketa.resume["status_id"]] }}
      </LabelSlot>
      <LabelSlot :label="'Дата создания'"
        >{{
          props.anketa.resume["created"]
            ? new Date(
                String(props.anketa.resume["created"])
              ).toLocaleDateString("ru-RU")
            : ""
        }}
      </LabelSlot>
      <LabelSlot :label="'Дата обновления'"
        >{{
          props.anketa.resume["updated"]
            ? new Date(
                String(props.anketa.resume["updated"])
              ).toLocaleDateString("ru-RU")
            : ""
        }}
      </LabelSlot>
      <LabelSlot :label="'Пользователь'">{{
        props.anketa.resume["user_id"]
      }}</LabelSlot>
      <LabelSlot :label="'Материалы'">
        <router-link
          v-if="props.anketa.resume['path']"
          :to="{
            name: 'manager',
            query: { path: props.anketa.resume['path'].split('/') },
          }"
        >
          {{ props.anketa.resume["path"] }}
        </router-link>
      </LabelSlot>
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

    <BtnGroup>
      <button
        :disabled="
          props.anketa.resume.user_id !== null &&
          props.anketa.resume.user_id !== ''
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
          storeClassify.classData.status[props.anketa.resume['status_id']] !==
            'Проверка' &&
          props.anketa.resume.user_id !== props.userId &&
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
    </BtnGroup>
  </div>
</template>
