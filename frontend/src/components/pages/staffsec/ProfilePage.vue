<script setup lang="ts">
import { defineAsyncComponent, ref, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
import { userStore } from "@/store/user";
import { server } from "@utilities/utils";
import { router } from "@/router/router";
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
} from "@/interfaces/interface";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const PhotoCard = defineAsyncComponent(
  () => import("@components/content/staffsec/divs//PhotoCard.vue")
);
const AnketaTab = defineAsyncComponent(
  () => import("@components/content/staffsec/tabs/AnketaTab.vue")
);
const CheckTab = defineAsyncComponent(
  () => import("@components/content/staffsec/tabs/CheckTab.vue")
);
const PoligrafTab = defineAsyncComponent(
  () => import("@components/content/staffsec/tabs/PoligrafTab.vue")
);
const InvestigateTab = defineAsyncComponent(
  () => import("@components/content/staffsec/tabs/InvestigateTab.vue")
);
const InquiryTab = defineAsyncComponent(
  () => import("@components/content/staffsec/tabs/InquiryTab.vue")
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
  imageUrl: "",
  printPage: false,
  spinner: false,
  resume: <Resume>{},
  staffs: [] as Array<Staff>,
  documents: [] as Array<Document>,
  addresses: [] as Array<Address>,
  contacts: [] as Array<Contact>,
  relations: [] as Array<Relation>,
  workplaces: [] as Array<Work>,
  affilations: [] as Array<Affilation>,
  checks: [] as Array<Verification>,
  robots: [] as Array<Robot>,
  poligraf: [] as Array<Pfo>,
  investigations: [] as Array<Inquisition>,
  inquiries: [] as Array<Needs>,
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
    anketaData.value.resume = response.data;

    if (action === "status") {
      storeAlert.alertMessage.setAlert("alert-info", "Статус анкеты обновлен");
    }
    if (action === "send") {
      storeAlert.alertMessage.setAlert(
        "alert-success",
        "Анкета отправлена на проверку"
      );
      window.scrollTo(0, 0);
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
    const response = await storeAuth.axiosInstance.get(
      `${server}/${param}/${candId}`
    );
    switch (param) {
      case "staff":
        anketaData.value.staffs = response.data;
        break;
      case "document":
        anketaData.value.documents = response.data;
        break;
      case "address":
        anketaData.value.addresses = response.data;
        break;
      case "contact":
        anketaData.value.contacts = response.data;
        break;
      case "relation":
        anketaData.value.relations = response.data;
        break;
      case "workplace":
        anketaData.value.workplaces = response.data;
        break;
      case "affilation":
        anketaData.value.affilations = response.data;
        break;
      case "check":
        anketaData.value.checks = response.data;
        break;
      case "robot":
        anketaData.value.robots = response.data;
        break;
      case "poligraf":
        anketaData.value.poligraf = response.data;
        break;
      case "investigation":
        anketaData.value.investigations = response.data;
        break;
      case "inquiry":
        anketaData.value.inquiries = response.data;
        break;
      case "file":
        anketaData.value.imageUrl = window.URL.createObjectURL(
          new Blob([response.data])
        );
        break;
      default:
        break;
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
    (anketaData.value.resume.status_id ===
      storeClassify.classData.status["finish"] ||
      anketaData.value.resume.status_id ===
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
      storeClassify.classData.status[anketaData.value.resume["status_id"]]
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
  <div class="container py-3">
    <PhotoCard
      :cand-id="candId"
      :image-url="anketaData.imageUrl"
      @get-item="getItem"
      @submit-file="submitFile"
    />
    <div class="position-relative">
      <div class="position-absolute top-0 end-0">
        <a
          href="#"
          class="d-print-none"
          @click="anketaData.printPage = !anketaData.printPage"
        >
          <i
            class="bi bi-printer fs-1"
            title="Версия для печати"
            style="cursor: pointer"
          >
          </i>
        </a>
      </div>
    </div>
    <HeaderDiv :page-header="anketaData.resume.fullname" />
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

    <div :class="{ 'tab-content': !anketaData.printPage }">
      <div
        id="anketaTab"
        :class="{ 'tab-pane fade py-1 show active': !anketaData.printPage }"
        :role="!anketaData.printPage ? 'tabpanel' : ''"
        :tabindex="!anketaData.printPage ? '0' : ''"
      >
        <AnketaTab
          :user-id="storeUser.userData.userId.toString()"
          :spinner="anketaData.spinner"
          :resume="anketaData.resume"
          :staffs="anketaData.staffs"
          :documents="anketaData.documents"
          :addresses="anketaData.addresses"
          :contacts="anketaData.contacts"
          :relations="anketaData.relations"
          :workplaces="anketaData.workplaces"
          :affilations="anketaData.affilations"
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
        <CheckTab
          :user-id="storeUser.userData.userId.toString()"
          :resume="anketaData.resume"
          :checks="anketaData.checks"
          :robots="anketaData.robots"
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
        <PoligrafTab
          :poligrafs="anketaData.poligraf"
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
        <InvestigateTab
          :inquisitions="anketaData.investigations"
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
        <InquiryTab
          :needs="anketaData.inquiries"
          @get-item="getItem"
          @delete="deleteItem"
          @submit="updateItem"
        />
      </div>
    </div>
  </div>
</template>
