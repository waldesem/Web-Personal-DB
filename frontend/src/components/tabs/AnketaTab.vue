<script setup lang="ts">
import { ref, defineAsyncComponent, inject, onBeforeMount } from "vue";
import { classifyStore } from "@/store/classify";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";
import { router } from "@/router/router";

const ResumeForm = defineAsyncComponent(
  () => import("@components/forms/ResumeForm.vue")
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
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);

const storeClassify = classifyStore();
const storeAuth = authStore();
const storeAlert = alertStore();

interface Resume {
  id: string;
  category_id: string;
  region_id: string;
  fullname: string;
  previous: string;
  birthday: string;
  birthplace: string;
  country: string;
  ext_country: string;
  snils: string;
  inn: string;
  education: string;
  marital: string;
  addition: string;
  path: string;
  status_id: string;
  created: string;
  updated: string;
  request_id: string;
}

const candId = inject("candId") as string;

onBeforeMount(() => {
  dataResume.value.getResume();
});

const dataResume = ref({
  resume: <Resume>{},
  action: "",
  item: "",
  spinner: false,
  form: <Record<string, any>>{},

  getResume: async function (action = "view"): Promise<void> {
    if (action === "status") {
      if (!confirm("Вы действительно хотите изменить статус резюме?")) {
        return;
      }
    }
    if (action === "send") {
      if (!confirm("Вы действительно хотите отправить анкету на проверку?")) {
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
        this.spinner = false;
        window.scrollTo(0, 0);
      }
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Ошибка обработки ${error}`
      );
    }
  },

  deleteResume: async function (): Promise<void> {
    if (
      ["robot", "finish"].includes(
        storeClassify.classData.status[this.resume["status_id"]]
      )
    ) {
      storeAlert.alertMessage.setAlert(
        "alert-warning",
        "Нельзя удалить запись с текущим статусом"
      );
      return;
    }

    if (confirm(`Вы действительно хотите удалить анкету?`)) {
      try {
        const response = await storeAuth.axiosInstance.delete(
          `${server}/resume`
        );
        console.log(response.status);
        router.push({ name: "persons", params: { group: "staffsec" } });

        storeAlert.alertMessage.setAlert(
          "alert-info",
          `Запись с ID ${candId} удалена`
        );
      } catch (error) {
        console.error(error);
      }
    }
  },

  deactivateForm: function () {
    this.action = "";
    this.item = "";
  },
});
</script>

<template>
  <div class="py-3">
    <template v-if="dataResume.item === 'resume'">
      <ResumeForm
        :get-item="dataResume.getResume"
        :action="dataResume.action"
        :cand-id="candId"
        :content="dataResume.resume"
        @deactivate="dataResume.deactivateForm"
      />
    </template>

    <template v-else>
      <div v-if="dataResume.resume">
        <RowDivSlot :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <a
              class="btn btn-link"
              title="Изменить"
              @click="dataResume.item = 'update'"
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot
          :label="'Категория'"
          :value="
            storeClassify.classData.category[dataResume.resume['category_id']]
          "
        />
        <RowDivSlot
          :label="'Регион'"
          :value="
            storeClassify.classData.regions[dataResume.resume['region_id']]
          "
        />
        <RowDivSlot
          :label="'Фамилия Имя Отчество'"
          :value="dataResume.resume['fullname']"
        />
        <RowDivSlot
          :label="'Изменение имени'"
          :value="dataResume.resume['previous']"
        />
        <RowDivSlot
          :label="'Дата рождения'"
          :value="dataResume.resume['birthday']"
        />
        <RowDivSlot
          :label="'Место рождения'"
          :value="dataResume.resume['birthplace']"
        />
        <RowDivSlot
          :label="'Гражданство'"
          :value="dataResume.resume['country']"
        />
        <RowDivSlot
          :label="'Второе гражданство'"
          :value="dataResume.resume['ext_country']"
        />
        <RowDivSlot :label="'СНИЛС'" :value="dataResume.resume['snils']" />
        <RowDivSlot :label="'ИНН'" :value="dataResume.resume['inn']" />
        <RowDivSlot
          :label="'Образование'"
          :value="dataResume.resume['education']"
        />
        <RowDivSlot
          :label="'Дополнительная информация'"
          :value="dataResume.resume['addition']"
        />
        <RowDivSlot :label="'Материалы'" :slotTwo="true" :print="true">
          <template v-slot:divTwo>
            <router-link
              :to="{
                name: 'manager',
                params: { group: 'staffsec' },
                query: { path: dataResume.resume['path'].split('/') },
              }"
            >
              {{ dataResume.resume["path"] }}
            </router-link>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Статус'" :slotTwo="true">
          <template v-slot:divTwo>
            <a href="#" @click="dataResume.getResume('status')">
              {{
                storeClassify.classData.status[dataResume.resume["status_id"]]
              }}
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot
          :label="'Создан'"
          :value="
            new Date(String(dataResume.resume['created'])).toLocaleDateString(
              'ru-RU'
            )
          "
        />
        <RowDivSlot
          :label="'Обновлен'"
          :value="
            new Date(String(dataResume.resume['updated'])).toLocaleDateString(
              'ru-RU'
            )
          "
        />
        <RowDivSlot
          :label="'Внешний ID'"
          :value="dataResume.resume['request_id']"
        />
      </div>
      <p v-else>Данные отсутствуют</p>
    </template>

    <StaffDiv />
    <DocumentDiv />
    <AddressDiv />
    <ContactDiv />
    <RelationDiv />
    <WorkplaceDiv />
    <AffilationDiv />

    <div class="d-print-none py-3">
      <div class="btn-group" role="group">
        <button
          class="btn btn-outline-primary"
          :disabled="
            (storeClassify.classData.status[dataResume.resume['status_id']] !==
              'new' &&
              storeClassify.classData.status[dataResume.resume['status_id']] !==
                'update' &&
              storeClassify.classData.status[dataResume.resume['status_id']] !==
                'repeat') ||
            dataResume.spinner
          "
          @click="dataResume.getResume('send')"
        >
          {{ !dataResume.spinner ? "Отправить на проверку" : "" }}
          <span
            v-if="dataResume.spinner"
            class="spinner-border spinner-border-sm"
          ></span>
          <span v-if="dataResume.spinner" role="status">Отправляется...</span>
        </button>
        <button
          type="button"
          class="btn btn-outline-danger"
          :disabled="
            storeClassify.classData.status[dataResume.resume['status_id']] ===
              'finish' || dataResume.spinner
          "
          @click="dataResume.deleteResume"
        >
          Удалить анкету
        </button>
      </div>
    </div>
  </div>
</template>
