<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { classifyStore } from "@/store/classify";
import type { Resume } from "@/interfaces/interface";

const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("../forms/ResumeForm.vue")
);
const StaffDiv = defineAsyncComponent(
  () => import("../divs/StaffDiv.vue")
);
const DocumentDiv = defineAsyncComponent(
  () => import("../divs/DocumentDiv.vue")
);
const AddressDiv = defineAsyncComponent(
  () => import("../divs/AddressDiv.vue")
);
const ContactDiv = defineAsyncComponent(
  () => import("../divs/ContactDiv.vue")
);
const RelationDiv = defineAsyncComponent(
  () => import("../divs/RelationDiv.vue")
);
const WorkplaceDiv = defineAsyncComponent(
  () => import("../divs/WorkplaceDiv.vue")
);
const AffilationDiv = defineAsyncComponent(
  () => import("../divs/AffilationDiv.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

const storeClassify = classifyStore();

const emit = defineEmits([
  "get-item", "get-resume", "delete", "submit", "file"
]);

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
    type: Object as () => Record<string, any>,
    default: () => {},
  },
  staffs: {
    type: Array as () => Array<Record<string, any>>,
    default: () => [],
  },
  documents: {
    type: Array as () => Array<Record<string, any>>,
    default: () => [],
  },
  addresses: {
    type: Array as () => Array<Record<string, any>>,
    default: () => [],
  },
  contacts: {
    type: Array as () => Array<Record<string, any>>,
    default: () => [],
  },
  relations: {
    type: Array as () => Array<Record<string, any>>,
    default: () => [],
  },
  workplaces: {
    type: Array as () => Array<Record<string, any>>,
    default: () => [],
  },
  affilations: {
    type: Array as () => Array<Record<string, any>>,
    default: () => [],
  },
});

const dataResume = ref({
  action: "",
  form: <Resume>{},
});

function getResume(action: string) {
  emit("get-resume", action)
};

function getItem(item: string) {
  emit("get-item", item)
};

function updateItem (
  action: string,
  item: string,
  itemId: string, 
  form: Object
  ) {
  emit("submit", [action, item, itemId, form])
};

function deleteItem(itemId: string, item: string){
  emit("delete", [itemId, item])
};
</script>

<template>
  <div class="py-3">
    <ModalWin
      :title="'Изменить запись'"
      :id="'modalAddress'"
      @cancel="dataResume.action = ''"
    >      
      <ResumeForm
        :action="dataResume.action"
        :cand-id="props.candId"
        :content="props.resume"
        @get-resume="getResume"
      />
    </ModalWin>

    <RowDivSlot :slotTwo="true" :print="true">
      <template v-slot:divTwo>
        <a
          class="btn btn-link"
          title="Изменить"
          @click="dataResume.action = 'update'"
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
        <a href="#" @click="getResume('status')">
          {{ storeClassify.classData.status[props.resume["status_id"]] }}
        </a>
      </template>
    </RowDivSlot>
    <RowDivSlot
      :label="'Создан'"
      :value="
        props.resume['created'] 
        ? new Date(String(props.resume['created'])).toLocaleDateString(
          'ru-RU'
        )
          : ''
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

    <StaffDiv
      :items="props.staffs"
      @get-item="getItem"
      @submit="updateItem"
      @delete="deleteItem"
    />
    <DocumentDiv
      :items="props.documents"
      @get-item="getItem"
      @update="updateItem"
      @delete="deleteItem"
    />
    <AddressDiv
      :items="props.addresses"
      @get-item="getItem"
      @update="updateItem"
      @delete="deleteItem"
    />
    <ContactDiv
      :items="props.contacts"
      @get-item="getItem"
      @update="updateItem"
      @delete="deleteItem"
    />
    <RelationDiv
      :items="props.relations"
      @get-item="getItem"
      @update="updateItem"
      @delete="deleteItem"
    />
    <WorkplaceDiv
      :items="props.workplaces"
      @get-item="getItem"
      @update="updateItem"
      @delete="deleteItem"
    />
    <AffilationDiv
      :items="props.affilations"
      @get-item="getItem"
      @update="updateItem"
      @delete="deleteItem"
    />

    <div class="d-print-none py-3">
      <BtnGroupForm :cls="false">
        <button
          :disabled="props.resume.user_id !== ''"
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
          @click="deleteItem(candId, 'resume')"
        >
          Удалить анкету
        </button>
      </BtnGroupForm>
    </div>
  </div>
</template>
