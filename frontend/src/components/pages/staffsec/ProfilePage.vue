<script setup lang="ts">
import { defineAsyncComponent, ref, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { axiosInstance } from "@/auth";
import { stateAlert, stateClassify, stateUser, stateAnketa } from "@/state";
import { server } from "@/utilities";
import { router } from "@/router";

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

const route = useRoute();

const candId = route.params.id.toString();

onBeforeMount(async () => {
  await getResume();
});

const pageDate = ref({
  printPage: false,
  spinner: false,
  imageUrl: "",
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
    pageDate.value.spinner = true;
    if (!confirm("Вы действительно хотите отправить анкету на проверку?")) {
      pageDate.value.spinner = false;
      return;
    }
  }
  if (action === "self") {
    if (!confirm("Вы действительно назначить проверку кандидата на себя?")) {
      return;
    }
  }
  try {
    const response = await axiosInstance.get(
      `${server}/resume/${candId}`,
      {
        params: {
          action: action,
        },
      }
    );
    stateAnketa.resume = response.data;

    if (["self", "send", "status"].includes(action)) {
      getResume("view");

      if (action === "status") {
        stateAlert.setAlert(
          "alert-info",
          "Статус анкеты обновлен"
        );
      }
      if (action === "self") {
        stateAlert.setAlert(
          "alert-info",
          "Анкета назначена на себя"
        );
      }
      if (action === "send") {
        stateAlert.setAlert(
          "alert-success",
          "Анкета отправлена на проверку"
        );
      }
    }
  } catch (error) {
    console.error(error);
    stateAlert.setAlert(
      "alert-danger",
      `Ошибка обработки ${error}`
    );
  }
  pageDate.value.spinner = false;
}

async function getItem(param: string): Promise<void> {
  try {
    const response =
      param === "image"
        ? await axiosInstance.get(`${server}/${param}/${candId}`, {
            responseType: "blob",
          })
        : await axiosInstance.get(`${server}/${param}/${candId}`);

    if (param === "image") {
      pageDate.value.imageUrl = window.URL.createObjectURL(
        new Blob([response.data], { type: "image/jpeg" })
      );
    } else {
      stateAnketa[param as keyof typeof stateAnketa] = response.data;
    }
  } catch (error) {
    console.error(error);
    stateAlert.setAlert("alert-danger", `Ошибка: ${error}`);
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
        ? await axiosInstance.post(
            `${server}/${param}/${candId}`,
            form
          )
        : await axiosInstance.patch(
            `${server}/${param}/${itemId}`,
            form
          );

    console.log(response.status);

    stateAlert.setAlert(
      "alert-success",
      "Данные успешно обновлены"
    );
    getItem(param);
  } catch (error) {
    stateAlert.setAlert(
      "alert-danger",
      `Возникла ошибка ${error}`
    );
  }
}

async function deleteItem(id: string, param: string): Promise<void> {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  if (
    param === "check" &&
    (stateAnketa.resume.status_id ===
      stateClassify.status["finish"] ||
      stateAnketa.resume.status_id ===
        stateClassify.status["robot"])
  ) {
    stateAlert.setAlert(
      "alert-warning",
      "Невозможно удалить проверку с текщим статусом"
    );
    return;
  }
  if (
    ["robot", "finish"].includes(
      stateClassify.status[
        stateAnketa.resume["status_id"]
      ]
    )
  ) {
    stateAlert.setAlert(
      "alert-warning",
      "Нельзя удалить запись с текущим статусом"
    );
    return;
  }
  try {
    const response = await axiosInstance.delete(
      `${server}/${param}/${id}`
    );
    console.log(response.status);

    param === "resume" ? router.push({ name: "persons" }) : getItem(param);

    stateAlert.setAlert("alert-info", `Запись с ID ${id} удалена`);
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
        stateAlert.setAlert(
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
      const response = await axiosInstance.post(
        `${server}/file/${param}/${candId}`,
        formData
      );
      console.log(response.status);
      if (param === "image") {
        getItem("file");
      }
      stateAlert.setAlert(
        "alert-success",
        "Файл или файлы успешно загружен/добавлены"
      );
    } catch (error) {
      console.error(error);
    }
  } else {
    stateAlert.setAlert(
      "alert-warning",
      "Ошибка при загрузке файла"
    );
  }
}
</script>

<template>
  <PhotoCard
    :cand-id="candId"
    :url="pageDate.imageUrl"
    @get-item="getItem"
    @submit-file="submitFile"
  />
  <div class="row mb-3">
    <div class="col-md-10">
      <HeaderDiv
        :page-header="`${stateAnketa.resume.surname} ${stateAnketa.resume.firstname} ${stateAnketa.resume.patronymic}`"
      />
    </div>
    <div class="col-md-2 d-flex justify-content-end d-print-none">
      <IconRelative
        :title="`Версия для печати`"
        :icon-class="`bi bi-printer fs-1`"
        @click="pageDate.printPage = !pageDate.printPage"
      />
      <IconRelative
        :title="`Взять на проверку`"
        :icon-class="`bi bi-person-plus fs-1`"
        :hide="
          stateAnketa.resume.user_id !== null &&
          stateAnketa.resume.user_id !== ''
        "
        @onclick="getResume('self')"
      />
      <IconRelative
        :title="`Отправить на проверку`"
        :icon-class="'bi bi-send-plus fs-1'"
        :hide="stateAnketa.resume.user_id !== stateUser.userId
        || stateAnketa.resume.status_id === stateClassify.status['robot']"
        @onclick="getResume('send')"
      >
        <span
          v-if="pageDate.spinner"
          class="spinner-border spinner-border-sm"
        ></span>
        <span v-if="pageDate.spinner" role="status">Отправляется...</span>
      </IconRelative>
    </div>
  </div>
  <div
    :class="{ 'nav nav-tabs nav-justified': !pageDate.printPage }"
    :role="!pageDate.printPage ? 'tablist' : ''"
  >
    <button
      v-if="!pageDate.printPage"
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
    :class="{ 'tab-content': !pageDate.printPage }">
    <div
      id="anketaTab"
      :class="{ 'tab-pane fade py-1 show active': !pageDate.printPage }"
      :role="!pageDate.printPage ? 'tabpanel' : ''"
      :tabindex="!pageDate.printPage ? '0' : ''"
    >
      <AnketaTab
        :print-page="pageDate.printPage"
        @get-resume="getResume"
        @get-item="getItem"
        @submit="updateItem"
        @delete="deleteItem"
      />
    </div>
    <div
      id="сheckTab"
      :class="{ 'tab-pane fade py-1': !pageDate.printPage }"
      :role="!pageDate.printPage ? 'tabpanel' : ''"
    >
      <h5 v-if="pageDate.printPage">Проверки</h5>
      <CheckTab
        :print-page="pageDate.printPage"
        @get-item="getItem"
        @delete="deleteItem"
        @submit="updateItem"
        @file="submitFile"
      />
    </div>
    <div
      id="poligrafTab"
      :class="{ 'tab-pane fade py-1': !pageDate.printPage }"
      :role="!pageDate.printPage ? 'tabpanel' : ''"
    >
      <h5 v-if="pageDate.printPage">Полиграф</h5>
      <PoligrafTab
        :print-page="pageDate.printPage"
        @get-item="getItem"
        @delete="deleteItem"
        @submit="updateItem"
        @file="submitFile"
      />
    </div>
    <div
      id="investigateTab"
      :class="{ 'tab-pane fade py-1': !pageDate.printPage }"
      :role="!pageDate.printPage ? 'tabpanel' : ''"
    >
      <h5 v-if="pageDate.printPage">Расследования</h5>
      <InvestigateTab
        :print-page="pageDate.printPage"
        @get-item="getItem"
        @delete="deleteItem"
        @submit="updateItem"
        @file="submitFile"
      />
    </div>
    <div
      id="inquiryTab"
      :class="{ 'tab-pane fade py-1': !pageDate.printPage }"
      :role="!pageDate.printPage ? 'tabpanel' : ''"
    >
      <h5 v-if="pageDate.printPage">Запросы</h5>
      <InquiryTab
        :print-page="pageDate.printPage"
        @get-item="getItem"
        @delete="deleteItem"
        @submit="updateItem"
      />
    </div>
  </div>
</template>
