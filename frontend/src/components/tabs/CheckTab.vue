<script setup lang="ts">
import { ref, defineAsyncComponent, inject, onBeforeMount } from "vue";
import { authStore } from "@store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";
import BtnGroupForm from "../elements/BtnGroupForm.vue";

const CheckForm = defineAsyncComponent(
  () => import("@components/forms/CheckForm.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const RobotDiv = defineAsyncComponent(
  () => import("@components/tabs/divs/RobotDiv.vue")
);

const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();

interface Verification {
  id: string;
  workplace: string;
  employee: string;
  document: string;
  inn: string;
  debt: string;
  bankruptcy: string;
  bki: string;
  courts: string;
  affiliation: string;
  terrorist: string;
  mvd: string;
  internet: string;
  cronos: string;
  cros: string;
  addition: string;
  pfo: string;
  conclusion: string;
  comments: string;
  deadline: string;
  officer: string;
}
  

onBeforeMount(() => {
  check.value.getItem();
});

const check = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Verification>{},
  items: Array<Verification>(),

  getItem: async function (param: string = ""): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/check/$/${candId}`, {
          params: {
            action: param
          }
        }
      );
      this.items = response.data;
    } catch (error) {
      console.error(error);
      storeAlert.alertMessage.setAlert(
        "alert-danger",
        `Ошибка: ${error}`
      );
    }
  },

  deleteItem: async function (id: string): Promise<void> {
    if (!confirm(`Вы действительно хотите удалить запись?`)) return;
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/check/${id}`
      );
      console.log(response.status);
      this.getItem();

      storeAlert.alertMessage.setAlert(
        "alert-info",
        `Запись с ID ${id} удалена`
      );
    } catch (error) {
      console.error(error);
    }
  },

  submitFile: async function (
      event: Event,
      idItem: string
    ): Promise<void> {
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
            `${server}/file/check/${idItem}`,
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

  deactivateForm: function () {
    this.isForm = false;
    this.action = "";
  },
});
</script>

<template>
  <div class="py-3">
    <template v-if="check.isForm">
      <CheckForm
        :get-item="check.getItem"
        :action="check.action"
        :cand-id="candId"
        :content="check.item"
        @deactivate="check.deactivateForm"
    />
    </template>
    <div v-else>
      <div v-if="check.items.length > 0">
        <CollapseDiv
          v-for="(item, idx) in check.items"
          :key="idx"
          :id="'check' + idx"
          :idx="idx"
          :label="'Проверка #' + (idx + 1)"
        >
          <RowDivSlot :slotTwo="true" :print="true">
            <template v-slot:divTwo>
              <a
                href="#"
                title="Удалить"
                @click="check.deleteItem(item['id'].toString())">
                <i class="bi bi-trash"></i> 
              </a>
              <a
                href="#"
                title="Изменить"
                @click="
                  check.isForm = true;
                  check.action = 'update';
                  check.item = item;
                  check.itemId = item['id'].toString();
                "
              >
                <i class="bi bi-pencil-square"></i>
            </a>
            </template>
          </RowDivSlot>
          <RowDivSlot
            :label="'Проверка по местам работы<'"
            :value="item['workplace']"
          />
          <RowDivSlot :label="'Бывший работник МТСБ'" :value="item['employee']" />
          <RowDivSlot :label="'Проверка паспорта'" :value="item['document']" />
          <RowDivSlot :label="'Проверка ИНН'" :value="item['inn']" />
          <RowDivSlot :label="'Проверка ФССП'" :value="item['debt']" />
          <RowDivSlot
            :label="'Проверка банкротства'"
            :value="item['bankruptcy']"
          />
          <RowDivSlot :label="'Проверка БКИ'" :value="item['bki']" />
          <RowDivSlot :label="'Проверка судебных дел'" :value="item['courts']" />
          <RowDivSlot
            :label="'Проверка аффилированности'"
            :value="item['affiliation']"
          />
          <RowDivSlot
            :label="'Проверка по списку террористов'"
            :value="item['terrorist']"
          />
          <RowDivSlot
            :label="'Проверка нахождения в розыске'"
            :value="item['mvd']"
          />
          <RowDivSlot
            :label="'Проверка в открытых источниках'"
            :value="item['internet']"
          />
          <RowDivSlot :label="'Проверка Кронос'" :value="item['cronos']" />
          <RowDivSlot :label="'Проверка Крос'" :value="item['cros']" />
          <RowDivSlot
            :label="'Дополнительная информация'"
            :value="item['addition']"
          />
          <RowDivSlot :label="'ПФО'" :value="item['pfo']" />
          <RowDivSlot :label="'Комментарии'" :value="item['comments']" />
          <RowDivSlot :label="'Результат проверки'" :value="item['conclusion']" />
          <RowDivSlot :label="'Сотрудник'" :value="item['officer']" />
          <RowDivSlot
            :label="'Дата'"
            :value="new Date(String(item['deadline'])).toLocaleDateString('ru-RU')"
          />
          <RowDivSlot :slotOne="true" :print="true">
            <form
              class="form"
              enctype="multipart/form-data"
              role="form"
              @change="
                check.submitFile(
                  $event,
                  item['id'].toString()
                )
              "
            >
              <input class="form-control" id="file" type="file" ref="file" multiple />
            </form>
          </RowDivSlot>
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
      <BtnGroupForm>
        <div class="d-print-none py-3">
          <a
            class="btn btn-outline-primary"
            type="button"
            @click="check.isForm = true; check.action = 'create'"
            >Добавить запись
          </a>
        </div>
      </BtnGroupForm>
      <RobotDiv />
    </div>
  </div>
</template>
