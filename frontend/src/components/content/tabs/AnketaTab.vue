<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { classifyStore } from "@/store/classify";
import type { Anketa, Resume } from "@/interfaces/interface";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
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
  printPage: {
    type: Boolean,
    default: false,
  },
  anketa: {
    type: Object as () => Anketa,
    default: {},
  },
});

const dataResume = ref({
  action: "",
  form: <Resume>{},
  showActions: false,
});

function submitForm(action: string, item: string, id: string, form: Object) {
  emit("submit", action, item, id, form);
};

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
      @get-resume="emit('get-resume', 'view')"
      @cancel="dataResume.action = ''; emit('get-resume')"
    />
    <div class="px-3" v-else
      @mouseover="dataResume.showActions = true"
      @mouseout="dataResume.showActions = false"
    > 
      <LabelSlot>
        <ActionIcons
          v-show="dataResume.showActions"
          @delete="emit('delete', props.anketa.resume['id'], 'resume')"
          @update="dataResume.action = 'update'"
          :disable="storeClassify.classData.status[props.anketa.resume['status_id']] ===
              'finish'
          "
        />
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
        props.anketa.resume["user_id"] ?
        storeClassify.classData.users[
          props.anketa.resume["user_id"]
        ] : ""
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
      :print-page="props.printPage"
      :items="props.anketa.staff"
      @get-item="emit('get-item', 'staff')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <DocumentDiv
      :print-page="props.printPage"
      :items="props.anketa.document"
      @get-item="emit('get-item', 'document')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <AddressDiv
      :print-page="props.printPage"
      :items="props.anketa.addresse"
      @get-item="emit('get-item', 'address')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <ContactDiv
      :print-page="props.printPage"
      :items="props.anketa.contact"
      @get-item="emit('get-item', 'contact')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <RelationDiv
      :print-page="props.printPage"
      :items="props.anketa.relation"
      @get-item="emit('get-item', 'relation')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <WorkplaceDiv
      :print-page="props.printPage"
      :items="props.anketa.workplace"
      @get-item="emit('get-item', 'workplace')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <AffilationDiv
      :print-page="props.printPage"
      :items="props.anketa.affilation"
      @get-item="emit('get-item', 'affilation')"
      @submit="submitForm"
      @delete="deleteItem"
    />
  </div>
</template>