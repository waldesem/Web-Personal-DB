<script setup lang="ts">
import { defineAsyncComponent, ref, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
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
  () => import("@components/layouts/PhotoCard.vue")
);
const AnketaTab = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/AnketaTab.vue")
);
const CheckTab = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/CheckTab.vue")
);
const PoligrafTab = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/PoligrafTab.vue")
);
const InvestigateTab = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/InvestigateTab.vue")
);
const InquiryTab = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/tabs/InquiryTab.vue")
);

const storeAuth = authStore();
const storeAlert = alertStore();
const storeClassify = classifyStore();

const route = useRoute();

const candId = route.params.id.toString();

onBeforeMount(async () => {
  await anketaData.value.getResume();
});

const anketaData = ref({
  imageUrl: "",
  printPage: false,
  spinner: false,
  tabsObject: {
    anketaTab: "Анкета",
    сheckTab: "Проверки",
    poligrafTab: "Полиграф",
    investigateTab: "Расследования",
    inquiryTab: "Запросы",
  },
  resume: <Resume>{},
  staffs: <Array<Staff>>[],
  documents: <Array<Document>>[],
  addresses: <Array<Address>>[],
  contacts: <Array<Contact>>[],
  relations: <Array<Relation>>[],
  workplaces: <Array<Work>>[],
  affilations: <Array<Affilation>>[],
  checks: Array<Verification>(),
  robots: Array<Robot>(),
  poligraf: Array<Pfo>(),
  investigations: Array<Inquisition>(),
  inquiries: Array<Needs>(),

  getResume: async function (action = "view"): Promise<void> {
    if (action === "status") {
      if (!confirm("Вы действительно хотите изменить статус резюме?")) {
        return;
      }
    }
    if (action === "send") {
      this.spinner = true;
      if (!confirm("Вы действительно хотите отправить анкету на проверку?")) {
        this.spinner = false;
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
      this.resume = response.data;

      if (action === "status") {
        storeAlert.alertMessage.setAlert(
          "alert-info",
          "Статус анкеты обновлен"
        );
      }
      if (action === "send") {
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Анкета отправлена на проверку"
        );
        window.scrollTo(0, 0);
        this.spinner = false;
      }
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Ошибка обработки ${error}`
      );
    }
    this.spinner = false;
  },

  getItem: async function (param: string): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/${param}/${candId}`
      );
      switch (param) {
        case "staff":
          this.staffs = response.data;
          break;
        case "document":
          this.documents = response.data;
          break;
        case "address":
          this.addresses = response.data;
          break;
        case "contact":
          this.contacts = response.data;
          break;
        case "relation":
          this.relations = response.data;
          break;
        case "workplace":
          this.workplaces = response.data;
          break;
        case "affilation":
          this.affilations = response.data;
          break;
        case "check":
          this.checks = response.data;
          break;
        case "robot":
          this.robots = response.data;
          break;
        case "poligraf":
          this.poligraf = response.data;
          break;
        case "investigation":
          this.investigations = response.data;
          break;
        case "inquiry":
          this.inquiries = response.data;
          break;
        case "file":
          this.imageUrl = window.URL.createObjectURL(new Blob([response.data]));
          break
        default:
          break;
      }
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert("alert-danger", `Ошибка: ${error}`);
    }
  },

  updateItem: async function (
    action: string,
    param: string,
    itemId: string,
    form: Object
  ): Promise<void> {
    try {
      const response =
        action === "create"
          ? await storeAuth.axiosInstance.post(
              `${server}/${param}/${itemId}`,
              form
            )
          : await storeAuth.axiosInstance.patch(
              `${server}/check/${itemId}`,
              form
            );

      console.log(response.status);

      storeAlert.alertMessage.setAlert(
        "alert-success",
        "Данные успешно обновлены"
      );
      this.getItem(param);
    } catch (error) {
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Возникла ошибка ${error}`
      );
    }
  },

  deleteItem: async function (id: string, param: string): Promise<void> {
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
      param === "resume"
        ? router.push({ name: "persons" })
        : this.getItem(param);

      storeAlert.alertMessage.setAlert(
        "alert-info",
        `Запись с ID ${id} удалена`
      );
    } catch (error) {
      console.error(error);
    }
  },

  submitFile: async function (event: Event, param: string): Promise<void> {
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
  },
});
</script>

<template>
  <div class="container py-3">
    <PhotoCard 
      :cand-id="candId" 
      :image-url="anketaData.imageUrl"
      :get-item="anketaData.getItem"
      :submit-file="anketaData.submitFile" 
    />
    <HeaderDiv :page-header="anketaData.resume.fullname" />
    <div
      v-if="!anketaData.printPage"
      :class="!anketaData.printPage ? 'nav nav-tabs nav-justified' : 'mt-1'"
      :role="anketaData.printPage ? 'tablist' : ''"
    >
      <div v-if="!anketaData.printPage">
        <button
          v-for="(value, key) in anketaData.tabsObject"
          class="nav-link"
          :class="{ active: key === 'anketaTab' }"
          data-bs-toggle="tab"
          :data-bs-target="`#${key}`"
          type="button"
          role="tab"
        >
          {{ value[0] }}
        </button>
      </div>
    </div>

    <div :class="!anketaData.printPage ? 'tab-content' : 'mt-1'">
      <div
        id="anketaTab"
        :class="
          anketaData.printPage ? 'tab-pane fade py-1 show active' : 'mt-1'
        "
        :role="anketaData.printPage ? 'tabpanel' : ''"
      >
        <AnketaTab
          :cand-id="candId"
          :spinner="anketaData.spinner"
          :resume="anketaData.resume"
          :staffs="anketaData.staffs"
          :documents="anketaData.documents"
          :addresses="anketaData.addresses"
          :contacts="anketaData.contacts"
          :relations="anketaData.relations"
          :workplaces="anketaData.workplaces"
          :affilations="anketaData.affilations"
          :get-resume="anketaData.getResume"
          :get-item="anketaData.getItem"
          :update-item="anketaData.updateItem"
          :delete-item="anketaData.deleteItem"
        />
      </div>
      <div
        id="сheckTab"
        :class="anketaData.printPage ? 'tab-pane fade py-1' : 'mt-1'"
        :role="anketaData.printPage ? 'tabpanel' : ''"
      >
        <CheckTab
          :cand-id="candId"
          :checks="anketaData.checks"
          :robots="anketaData.robots"
          :get-item="anketaData.getItem"
          :update-item="anketaData.updateItem"
          :delete-item="anketaData.deleteItem"
          :submit-file="anketaData.submitFile"
          :status-id="anketaData.resume.status_id"
          :user-id="anketaData.resume.user_id"
        />
      </div>
      <div
        id="poligrafTab"
        :class="anketaData.printPage ? 'tab-pane fade py-1' : 'mt-1'"
        :role="anketaData.printPage ? 'tabpanel' : ''"
      >
        <PoligrafTab
          :cand-id="candId"
          :poligraf="anketaData.poligraf"
          :get-item="anketaData.getItem"
          :update-item="anketaData.updateItem"
          :delete-item="anketaData.deleteItem"
          :submit-file="anketaData.submitFile"
        />
      </div>
      <div
        id="investigateTab"
        :class="anketaData.printPage ? 'tab-pane fade py-1' : 'mt-1'"
        :role="anketaData.printPage ? 'tabpanel' : ''"
      >
        <InvestigateTab
          :cand-id="candId"
          :investigations="anketaData.investigations"
          :get-item="anketaData.getItem"
          :update-item="anketaData.updateItem"
          :delete-item="anketaData.deleteItem"
          :submit-file="anketaData.submitFile"
        />
      </div>
      <div
        id="inquiryTab"
        :class="anketaData.printPage ? 'tab-pane fade py-1' : 'mt-1'"
        :role="anketaData.printPage ? 'tabpanel' : ''"
      >
        <InquiryTab
          :cand-id="candId"
          :inquiries="anketaData.inquiries"
          :get-item="anketaData.getItem"
          :update-item="anketaData.updateItem"
          :delete-item="anketaData.deleteItem"
          :submit-file="anketaData.submitFile"
        />
      </div>
    </div>
    <a
      href="#"
      class="d-print-none"
      @click="anketaData.printPage = !anketaData.printPage"
    >
      <i class="bi bi-printer fs-1" title="Версия для печати"></i>
    </a>
  </div>
</template>

<style scoped>
.bi-printer {
  position: fixed;
  top: 80px;
  right: 40px;
  z-index: 9999;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
}
</style>
@/store/auth