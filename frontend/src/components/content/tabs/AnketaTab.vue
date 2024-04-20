<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { stateClassify, stateAnketa } from "@/state";
import type { Resume } from "@/interfaces";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("@components/content/forms/ResumeForm.vue")
);
const PreviousDiv = defineAsyncComponent(
  () => import("@components/content/divs/PreviousDiv.vue")
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
      :resume="stateAnketa.resume"
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
          @delete="emit('delete', stateAnketa.resume['id'], 'resume')"
          @update="dataResume.action = 'update'"
          :disable="stateClassify.status[stateAnketa.resume['status_id']] ===
              'finish'
          "
        />
      </LabelSlot>
      <LabelSlot :label="'ID'">{{ stateAnketa.resume["id"] }}</LabelSlot>
      <LabelSlot :label="'Фамилия'">{{
        stateAnketa.resume["surname"]
      }}</LabelSlot>
      <LabelSlot :label="'Имя'">{{
        stateAnketa.resume["firstname"]
      }}</LabelSlot>
      <LabelSlot :label="'Отчество'">{{
        stateAnketa.resume["patronymic"]
      }}</LabelSlot>
      <LabelSlot :label="'Дата рождения'"
        >{{
          new Date(String(stateAnketa.resume["birthday"])).toLocaleDateString(
            "ru-RU"
          )
        }}
      </LabelSlot>
      <LabelSlot :label="'Место рождения'">{{
        stateAnketa.resume["birthplace"]
      }}</LabelSlot>
      <LabelSlot :label="'Гражданство'">{{
        stateAnketa.resume["country"]
      }}</LabelSlot>
      <LabelSlot :label="'Двойное гражданство'"
        >{{ stateAnketa.resume["ext_country"] }}
      </LabelSlot>
      <LabelSlot :label="'СНИЛС'">{{
        stateAnketa.resume["snils"]
      }}</LabelSlot>
      <LabelSlot :label="'ИНН'">{{ stateAnketa.resume["inn"] }}</LabelSlot>
      <LabelSlot :label="'Образование'"
        >{{ stateAnketa.resume["education"] }}
      </LabelSlot>
      <LabelSlot :label="'Семейнное положение'"
        >{{ stateAnketa.resume["marital"] }}
      </LabelSlot>
      <LabelSlot :label="'Дополнительная информация'"
        >{{ stateAnketa.resume["addition"] }}
      </LabelSlot>
      <LabelSlot :label="'Статус'"
        >{{ stateClassify.status[stateAnketa.resume["status_id"]] }}
      </LabelSlot>
      <LabelSlot :label="'Дата создания'"
        >{{
          stateAnketa.resume["created"]
            ? new Date(
                String(stateAnketa.resume["created"])
              ).toLocaleDateString("ru-RU")
            : ""
        }}
      </LabelSlot>
      <LabelSlot :label="'Дата обновления'"
        >{{
          stateAnketa.resume["updated"]
            ? new Date(
                String(stateAnketa.resume["updated"])
              ).toLocaleDateString("ru-RU")
            : ""
        }}
      </LabelSlot>
      <LabelSlot :label="'Пользователь'">{{
        stateAnketa.resume["user_id"] ?
        stateClassify.users[
          stateAnketa.resume["user_id"]
        ] : ""
      }}</LabelSlot>
      <LabelSlot :label="'Материалы'">
        <router-link
          v-if="stateAnketa.resume['path']"
          :to="{
            name: 'manager',
            query: { path: stateAnketa.resume['path'].split('/') },
          }"
        >
          {{ stateAnketa.resume["path"] }}
        </router-link>
      </LabelSlot>
    </div>
    <hr/>
    <PreviousDiv
      :print-page="props.printPage"
      @get-item="emit('get-item', 'previous')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <StaffDiv
      :print-page="props.printPage"
      @get-item="emit('get-item', 'staff')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <DocumentDiv
      :print-page="props.printPage"
      @get-item="emit('get-item', 'document')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <AddressDiv
      :print-page="props.printPage"
      @get-item="emit('get-item', 'address')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <ContactDiv
      :print-page="props.printPage"
      @get-item="emit('get-item', 'contact')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <RelationDiv
      :print-page="props.printPage"
      @get-item="emit('get-item', 'relation')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <WorkplaceDiv
      :print-page="props.printPage"
      @get-item="emit('get-item', 'workplace')"
      @submit="submitForm"
      @delete="deleteItem"
    />
    <AffilationDiv
      :print-page="props.printPage"
      @get-item="emit('get-item', 'affilation')"
      @submit="submitForm"
      @delete="deleteItem"
    />
  </div>
</template>