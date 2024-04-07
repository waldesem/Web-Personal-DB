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

const storeClassify = classifyStore();

const emit = defineEmits([
  "get-item",
  "get-resume",
  "delete",
  "submit",
  "file",
]);

const props = defineProps({
  anketa: {
    type: Object as () => Anketa,
    default: {},
  },
});

const dataResume = ref({
  action: "",
  form: <Resume>{},
  showActions: false,
  handleMouse() {
    this.showActions = !this.showActions;
  }
});

function submitForm(action: string, item: string, id: string, form: Object) {
  emit("submit", action, item, id, form);
};

function deleteItem(itemId: string, item: string) {
  emit("delete", itemId, item);
}
</script>

<template>
  <div class="py-3" :class="{ 'border border-primary rounded': dataResume.showActions }">
    <ResumeForm
      v-if="dataResume.action"
      :action="dataResume.action"
      :resume="props.anketa.resume"
      @get-resume="emit('get-resume')"
      @cancel="dataResume.action = ''"
    />
    <div v-else
      @mouseover="dataResume.handleMouse"
      @mouseout="dataResume.handleMouse"
    >
      <LabelSlot v-show="!dataResume.showActions">
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
              'finish'
          "
          @click="emit('delete', props.anketa.resume['id'], 'resume')"
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
    <hr/>
    <StaffDiv
      :items="props.anketa.staffs"
      @get-item="emit('get-item', 'staff')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <hr/>
    <DocumentDiv
      :items="props.anketa.documents"
      @get-item="emit('get-item', 'document')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <hr/>
    <AddressDiv
      :items="props.anketa.addresses"
      @get-item="emit('get-item', 'address')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <hr/>
    <ContactDiv
      :items="props.anketa.contacts"
      @get-item="emit('get-item', 'contact')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <hr/>
    <RelationDiv
      :items="props.anketa.relations"
      @get-item="emit('get-item', 'relation')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <hr/>
    <WorkplaceDiv
      :items="props.anketa.workplaces"
      @get-item="emit('get-item', 'workplace')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <hr/>
    <AffilationDiv
      :items="props.anketa.affilations"
      @get-item="emit('get-item', 'affilation')"
      @submit="submitForm"
      @delete="deleteItem"
    />
  </div>
</template>
