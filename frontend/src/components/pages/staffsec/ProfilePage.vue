<script setup lang="ts">
import { defineAsyncComponent, ref, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
import { userStore } from "@/store/user";
import { server } from "@/utilities";
import { router } from "@/router";
import {
  Resume,
  Staff,
  Document,
  Address,
  Contact,
  Relation,
  Work,
  Affilation,
  Verification,
  Robot,
  Pfo,
  Inquisition,
  Needs,
} from "@/interfaces";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const IconRelative = defineAsyncComponent(
  () => import("@components/content/elements/IconRelative.vue")
);
const PhotoCard = defineAsyncComponent(
  () => import("@components/content/divs//PhotoCard.vue")
);
const AnketaTab = defineAsyncComponent(
  () => import("@components/content/tabs/AnketaTab.vue")
);
const CheckTab = defineAsyncComponent(
  () => import("@components/content/tabs/CheckTab.vue")
);
const PoligrafTab = defineAsyncComponent(
  () => import("@components/content/tabs/PoligrafTab.vue")
);
const InvestigateTab = defineAsyncComponent(
  () => import("@components/content/tabs/InvestigateTab.vue")
);
const InquiryTab = defineAsyncComponent(
  () => import("@components/content/tabs/InquiryTab.vue")
);

const storeAuth = authStore();
const storeAlert = alertStore();
const storeClassify = classifyStore();
const storeUser = userStore();

const route = useRoute();

const candId = route.params.id.toString();

onBeforeMount(async () => {
  await getResume();
});

const anketaData = ref({
  printPage: false,
  spinner: false,
  imageUrl: "",
  anketa: {
    resume: <Resume>{},
    staff: [] as Array<Staff>,
    document: [] as Array<Document>,
    addresse: [] as Array<Address>,
    contact: [] as Array<Contact>,
    relation: [] as Array<Relation>,
    workplace: [] as Array<Work>,
    affilation: [] as Array<Affilation>,
    check: [] as Array<Verification>,
    robot: [] as Array<Robot>,
    poligraf: [] as Array<Pfo>,
    investigation: [] as Array<Inquisition>,
    inquiry: [] as Array<Needs>,
  },
});

async function getResume(action = "view"): Promise<void> {
  if (action === "status") {
    if (
      !confirm(
        "Вы действительно хотите изменить статус? USER_ID анкеты будет сброшен"
      )
    ) {
      return;
    }
  }
  if (action === "send") {
    anketaData.value.spinner = true;
    if (!confirm("Вы действительно хотите отправить анкету на проверку?")) {
      anketaData.value.spinner = false;
      return;
    }
  }
  if (action === "self") {
    if (!confirm("Вы действительно назначить проверку кандидата на себя?")) {
      return;
    }
  }
  try {
    const response = await storeAuth.axiosInstance.get(
      `${server}/resume/${candId}`,
      {
        params: {
          action: action,
        },
      }
    );
    anketaData.value.anketa.resume = response.data;

    if (["self", "send", "status"].includes(action)) {
      getResume("view");

      if (action === "status") {
        storeAlert.alertMessage.setAlert(
          "alert-info",
          "Статус анкеты обновлен"
        );
      }
      if (action === "self") {
        storeAlert.alertMessage.setAlert(
          "alert-info",
          "Анкета назначена на себя"
        );
      }
      if (action === "send") {
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Анкета отправлена на проверку"
        );
      }
    }
  } catch (error) {
    console.error(error);
    storeAlert.alertMessage.setAlert(
      "alert-danger",
      `Ошибка обработки ${error}`
    );
  }
  anketaData.value.spinner = false;
}

async function getItem(param: string): Promise<void> {
  try {
    const response =
      param === "image"
        ? await storeAuth.axiosInstance.get(`${server}/${param}/${candId}`, {
            responseType: "blob",
          })
        : await storeAuth.axiosInstance.get(`${server}/${param}/${candId}`);

    if (param === "image") {
      anketaData.value.imageUrl = window.URL.createObjectURL(
        new Blob([response.data], { type: "image/jpeg" })
      );
    } else {
      anketaData.value.anketa[param as keyof typeof anketaData.value.anketa] =
        response.data;
    }
  } catch (error) {
    console.error(error);
    storeAlert.alertMessage.setAlert("alert-danger", `Ошибка: ${error}`);
  }
}

async function updateItem(
  action: string,
  param: string,
  itemId: string,
  form: Object
): Promise<void> {
  try {
    const response =
      action === "create"
        ? await storeAuth.axiosInstance.post(
            `${server}/${param}/${candId}`,
            form
          )
        : await storeAuth.axiosInstance.patch(
            `${server}/${param}/${itemId}`,
            form
          );

    console.log(response.status);

    storeAlert.alertMessage.setAlert(
      "alert-success",
      "Данные успешно обновлены"
    );
    getItem(param);
  } catch (error) {
    storeAlert.alertMessage.setAlert(
      "alert-danger",
      `Возникла ошибка ${error}`
    );
  }
}

async function deleteItem(id: string, param: string): Promise<void> {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  if (
    param === "check" &&
    (anketaData.value.anketa.resume.status_id ===
      storeClassify.classData.status["finish"] ||
      anketaData.value.anketa.resume.status_id ===
        storeClassify.classData.status["robot"])
  ) {
    storeAlert.alertMessage.setAlert(
      "alert-warning",
      "Невозможно удалить проверку с текщим статусом"
    );
    return;
  }
  if (
    ["robot", "finish"].includes(
      storeClassify.classData.status[
        anketaData.value.anketa.resume["status_id"]
      ]
    )
  ) {
    storeAlert.alertMessage.setAlert(
      "alert-warning",
      "Нельзя удалить запись с текущим статусом"
    );
    return;
  }
  try {
    const response = await storeAuth.axiosInstance.delete(
      `${server}/${param}/${id}`
    );
    console.log(response.status);

    param === "resume" ? router.push({ name: "persons" }) : getItem(param);

    storeAlert.alertMessage.setAlert("alert-info", `Запись с ID ${id} удалена`);
  } catch (error) {
    console.error(error);
  }
}

async function submitFile(event: Event, param: string): Promise<void> {
  const inputElement = event.target as HTMLInputElement;
  if (inputElement && inputElement.files && inputElement.files.length > 0) {
    const maxSizeInBytes = 1024 * 1024; // 1MB
    for (let i = 0; i < inputElement.files.length; i++) {
      if (inputElement.files[i].size > maxSizeInBytes) {
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "File size exceeds the limit. Please select a smaller file."
        );
        inputElement.value = ""; // Reset the input field
        return;
      }
    }
    const formData = new FormData();
    formData.append("file", inputElement.files[0]);

    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/file/${param}/${candId}`,
        formData
      );
      console.log(response.status);
      if (param === "image") {
        getItem("file");
      }
      storeAlert.alertMessage.setAlert(
        "alert-success",
        "Файл или файлы успешно загружен/добавлены"
      );
    } catch (error) {
      console.error(error);
    }
  } else {
    storeAlert.alertMessage.setAlert(
      "alert-warning",
      "Ошибка при загрузке файла"
    );
  }
}
</script>

<template>
  <PhotoCard
    :cand-id="candId"
    :url="anketaData.imageUrl"
    @get-item="getItem"
    @submit-file="submitFile"
  />
  <div class="row mb-3">
    <div class="col-md-10">
      <HeaderDiv
        :page-header="`${anketaData.anketa.resume.surname} ${anketaData.anketa.resume.firstname} ${anketaData.anketa.resume.patronymic}`"
      />
    </div>
    <div class="col-md-2 d-flex justify-content-end d-print-none">
      <IconRelative
        :title="`Версия для печати`"
        :icon-class="`bi bi-printer fs-1`"
        @click="anketaData.printPage = !anketaData.printPage"
      />
      <IconRelative
        :title="`Взять на проверку`"
        :icon-class="`bi bi-person-plus fs-1`"
        :hide="
          anketaData.anketa.resume.user_id !== null &&
          anketaData.anketa.resume.user_id !== ''
        "
        @onclick="getResume('self')"
      />
      <IconRelative
        :title="`Отправить на проверку`"
        :icon-class="'bi bi-send-plus fs-1'"
        :hide="anketaData.anketa.resume.user_id !== storeUser.userData.userId
        || anketaData.anketa.resume.status_id === storeClassify.classData.status['robot']"
        @onclick="getResume('send')"
      >
        <span
          v-if="anketaData.spinner"
          class="spinner-border spinner-border-sm"
        ></span>
        <span v-if="anketaData.spinner" role="status">Отправляется...</span>
      </IconRelative>
    </div>
  </div>
  <div
    :class="{ 'nav nav-tabs nav-justified': !anketaData.printPage }"
    :role="!anketaData.printPage ? 'tablist' : ''"
  >
    <button
      v-if="!anketaData.printPage"
      v-for="(value, key) in {
        anketaTab: 'Анкета',
        сheckTab: 'Проверки',
        poligrafTab: 'Полиграф',
        investigateTab: 'Расследования',
        inquiryTab: 'Запросы',
      }"
      class="nav-link"
      :class="{ active: key === 'anketaTab' }"
      :data-bs-target="`#${key}`"
      data-bs-toggle="tab"
      type="button"
      role="tab"
    >
      {{ value }}
    </button>
  </div>

  <div 
    :class="{ 'tab-content': !anketaData.printPage }">
    <div
      id="anketaTab"
      :class="{ 'tab-pane fade py-1 show active': !anketaData.printPage }"
      :role="!anketaData.printPage ? 'tabpanel' : ''"
      :tabindex="!anketaData.printPage ? '0' : ''"
    >
      <AnketaTab
        :print-page="anketaData.printPage"
        :anketa="anketaData.anketa"
        @get-resume="getResume"
        @get-item="getItem"
        @submit="updateItem"
        @delete="deleteItem"
      />
    </div>
    <div
      id="сheckTab"
      :class="{ 'tab-pane fade py-1': !anketaData.printPage }"
      :role="!anketaData.printPage ? 'tabpanel' : ''"
    >
      <h5 v-if="anketaData.printPage">Проверки</h5>
      <CheckTab
        :print-page="anketaData.printPage"
        :user-id="storeUser.userData.userId.toString()"
        :anketa="anketaData.anketa"
        @get-item="getItem"
        @delete="deleteItem"
        @submit="updateItem"
        @file="submitFile"
      />
    </div>
    <div
      id="poligrafTab"
      :class="{ 'tab-pane fade py-1': !anketaData.printPage }"
      :role="!anketaData.printPage ? 'tabpanel' : ''"
    >
      <h5 v-if="anketaData.printPage">Полиграф</h5>
      <PoligrafTab
        :print-page="anketaData.printPage"
        :poligrafs="anketaData.anketa.poligraf"
        @get-item="getItem"
        @delete="deleteItem"
        @submit="updateItem"
        @file="submitFile"
      />
    </div>
    <div
      id="investigateTab"
      :class="{ 'tab-pane fade py-1': !anketaData.printPage }"
      :role="!anketaData.printPage ? 'tabpanel' : ''"
    >
      <h5 v-if="anketaData.printPage">Расследования</h5>
      <InvestigateTab
        :print-page="anketaData.printPage"
        :inquisitions="anketaData.anketa.investigation"
        @get-item="getItem"
        @delete="deleteItem"
        @submit="updateItem"
        @file="submitFile"
      />
    </div>
    <div
      id="inquiryTab"
      :class="{ 'tab-pane fade py-1': !anketaData.printPage }"
      :role="!anketaData.printPage ? 'tabpanel' : ''"
    >
      <h5 v-if="anketaData.printPage">Запросы</h5>
      <InquiryTab
        :print-page="anketaData.printPage"
        :needs="anketaData.anketa.inquiry"
        @get-item="getItem"
        @delete="deleteItem"
        @submit="updateItem"
      />
    </div>
  </div>
</template>
