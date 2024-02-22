<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { profileStore } from "@/store/profile";
import { classifyStore } from "@/store/classify";
import { clearForm } from "@utilities/utils";

const SwitchBtnForm = defineAsyncComponent(
  () => import("@components/elements/SwitchBtnForm.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const ResumeDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/ResumeDiv.vue")
);
const StaffDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/StaffDiv.vue")
);
const DocumentDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/DocumentDiv.vue")
);
const AddressDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/AddressDiv.vue")
);
const ContactDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/ContactDiv.vue")
);
const RelationDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/RelationDiv.vue")
);
const WorkplaceDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/WorkplaceDiv.vue")
);
const AffilationDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/AffilationDiv.vue")
);
const ResumeForm = defineAsyncComponent(
  () => import("@components/forms/ResumeForm.vue")
);
const DocumentForm = defineAsyncComponent(
  () => import("@components/forms/DocumentForm.vue")
);
const AddressForm = defineAsyncComponent(
  () => import("@components/forms/AddressForm.vue")
);
const ContactForm = defineAsyncComponent(
  () => import("@components/forms/ContactForm.vue")
);
const RelationForm = defineAsyncComponent(
  () => import("@components/forms/RelationForm.vue")
);
const WorkplaceForm = defineAsyncComponent(
  () => import("@components/forms/WorkplaceForm.vue")
);
const AffilationForm = defineAsyncComponent(
  () => import("@components/forms/AffilationForm.vue")
);

const storeProfile = profileStore();
const storeClassify = classifyStore();

const hiddenSendBtn = ref(false);
const hiddenDelBtn = ref(false);

hiddenSendBtn.value =
  (storeClassify.classData.status[
    storeProfile.dataResume.resume["status_id"]
  ] !== "new" &&
    storeClassify.classData.status[
      storeProfile.dataResume.resume["status_id"]
    ] !== "update" &&
    storeClassify.classData.status[
      storeProfile.dataResume.resume["status_id"]
    ] !== "repeat") ||
  storeProfile.dataProfile.spinner;

hiddenDelBtn.value =
  storeClassify.classData.status[
    storeProfile.dataResume.resume["status_id"]
  ] === "finish" || storeProfile.dataProfile.spinner;

function switchForm(item: string) {
  storeProfile.dataProfile.item === item
    ? (storeProfile.dataProfile.item = "")
    : (storeProfile.dataProfile.item = item);

  storeProfile.dataProfile.item === item
    ? (storeProfile.dataProfile.action = "create")
    : (storeProfile.dataProfile.action = "");

  clearForm(storeProfile.dataProfile.form);
}
</script>

<template>
  <div class="py-3">
    <template
      v-if="
        storeProfile.dataProfile.item === 'resume' &&
        storeProfile.dataProfile.action === 'update'
      "
    >
      <ResumeForm />
    </template>

    <template v-else>
      <RegionForm />
      <ResumeDiv v-if="storeProfile.dataResume.resume" />
      <p v-else>Данные отсутствуют</p>
    </template>

    <StaffDiv />

    <h6>
      Документы
      <SwitchBtnForm
        :item="'document'"
        :switchForm="switchForm"
        :subj="storeProfile.dataProfile.item"
      />
    </h6>
    <template v-if="storeProfile.dataProfile.item === 'document'">
      <DocumentForm />
    </template>
    <template v-else>
      <div v-if="storeProfile.dataAnketa.docums.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataAnketa.docums"
          :key="idx"
          :id="'docum' + idx"
          :idx="idx"
          :label="'Документ #' + (idx + 1)"
        >
          <DocumentDiv :item="item" />
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <h6>
      Адреса
      <SwitchBtnForm
        :item="'address'"
        :switchForm="switchForm"
        :subj="storeProfile.dataProfile.item"
      />
    </h6>
    <template v-if="storeProfile.dataProfile.item === 'address'">
      <AddressForm />
    </template>
    <template v-else>
      <div v-if="storeProfile.dataAnketa.addrs.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataAnketa.addrs"
          :key="idx"
          :id="'addr' + idx"
          :idx="idx"
          :label="'Адрес #' + (idx + 1)"
        >
          <AddressDiv :item="item" />
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <h6>
      Контакты
      <SwitchBtnForm
        :item="'contact'"
        :switchForm="switchForm"
        :subj="storeProfile.dataProfile.item"
      />
    </h6>
    <template v-if="storeProfile.dataProfile.item === 'contact'">
      <ContactForm />
    </template>
    <template v-else>
      <div v-if="storeProfile.dataAnketa.conts.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataAnketa.conts"
          :key="idx"
          :id="'cont' + idx"
          :idx="idx"
          :label="'Контакт #' + (idx + 1)"
        >
          <ContactDiv :item="item" />
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <h6>
      Работа
      <SwitchBtnForm
        :item="'workplace'"
        :switchForm="switchForm"
        :subj="storeProfile.dataProfile.item"
      />
    </h6>
    <template v-if="storeProfile.dataProfile.item === 'workplace'">
      <WorkplaceForm />
    </template>
    <template v-else>
      <div v-if="storeProfile.dataAnketa.works.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataAnketa.works"
          :key="idx"
          :id="'work' + idx"
          :idx="idx"
          :label="'Работа #' + (idx + 1)"
        >
          <WorkplaceDiv :item="item" />
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <h6>
      Аффилированность
      <SwitchBtnForm
        :item="'affilation'"
        :switchForm="switchForm"
        :subj="storeProfile.dataProfile.item"
      />
    </h6>
    <template v-if="storeProfile.dataProfile.item === 'affilation'">
      <AffilationForm />
    </template>
    <template v-else>
      <div v-if="storeProfile.dataAnketa.affilation.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataAnketa.affilation"
          :key="idx"
          :id="'affil' + idx"
          :idx="idx"
          :label="'Аффилированность #' + (idx + 1)"
        >
          <AffilationDiv :item="item" />
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <h6>
      Связи
      <SwitchBtnForm
        :item="'relation'"
        :switchForm="switchForm"
        :subj="storeProfile.dataProfile.item"
      />
    </h6>
    <template v-if="storeProfile.dataProfile.item === 'relation'">
      <RelationForm />
    </template>
    <template v-else>
      <div v-if="storeProfile.dataAnketa.relate.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataAnketa.relate"
          :key="idx"
          :id="'relate' + idx"
          :idx="idx"
          :label="'Связь #' + (idx + 1)"
        >
          <RelationDiv :item="item" />
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <div class="d-print-none py-3">
      <div class="btn-group" role="group">
        <button
          class="btn btn-outline-primary"
          :disabled="hiddenSendBtn"
          @click="storeProfile.dataResume.getResume('send')"
        >
          {{ !storeProfile.dataProfile.spinner ? "Отправить на проверку" : "" }}
          <span
            v-if="storeProfile.dataProfile.spinner"
            class="spinner-border spinner-border-sm"
          ></span>
          <span v-if="storeProfile.dataProfile.spinner" role="status"
            >Отправляется...</span
          >
        </button>
        <button
          type="button"
          class="btn btn-outline-danger"
          :disabled="hiddenDelBtn"
          @click="storeProfile.dataResume.deleteResume"
        >
          Удалить анкету
        </button>
      </div>
    </div>
  </div>
</template>
