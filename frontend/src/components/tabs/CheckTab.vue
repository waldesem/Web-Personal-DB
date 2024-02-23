<script setup lang="ts">
import { ref, defineAsyncComponent, inject, onBeforeMount } from "vue";
import { classifyStore } from "@store/classify";
import { authStore } from "@store/token";
import { alertStore } from "@store/alert";
import { server } from "@utilities/utils";

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


const hiddenAddBtn = ref(false);
const hiddenDelBtn = ref(false);
const hiddenEditBtn = ref(false);

hiddenDelBtn.value =
  storeProfile.dataProfile.resume["status"] ===
    storeClassify.classData.status["finish"] ||
  storeProfile.dataProfile.resume["status"] ===
    storeClassify.classData.status["robot"];

hiddenEditBtn.value =
  storeProfile.dataProfile.resume["status"] !==
    storeClassify.classData.status["save"] &&
  storeProfile.dataProfile.resume["status"] !==
    storeClassify.classData.status["cancel"] &&
  storeProfile.dataProfile.resume["status"] !==
    storeClassify.classData.status["manual"];

hiddenAddBtn.value = ![
  storeClassify.classData.status["new"],
  storeClassify.classData.status["update"],
  storeClassify.classData.status["save"],
  storeClassify.classData.status["repeat"],
].includes(storeProfile.dataProfile.resume["status"]);


const candId = inject("candId") as string;
const storeAuth = authStore();
const storeAlert = alertStore();
const storeClassify = classifyStore();

interface Staff {
  id: string;
  position: string;
  department: string;
}

onBeforeMount(() => {
  check.value.getItem();
});

const check = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Staff>{},
  items: Array<Staff>(),

  getItem: async function (): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/check/${candId}`
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

  deactivateForm: function () {
    this.isForm = false;
    this.action = "";
  },
});
</script>

<template>
  <div class="py-3">
    <CheckForm
      v-if="
        storeProfile.dataProfile.action === 'update' &&
        storeProfile.dataProfile.flag === 'check'
      "
    />
    <div v-else>
      <div v-if="storeProfile.dataProfile.verification.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataProfile.verification"
          :key="idx"
          :id="'check' + idx"
          :idx="idx"
          :label="'Проверка #' + (idx + 1)"
        >
          <RowDivSlot :slotTwo="true" :print="true">
            <template v-slot:divTwo>
              <a
                :hidden="hiddenDelBtn"
                href="#"
                title="Удалить"
                @click="
                  storeProfile.dataProfile.deleteItem(
                    props.item['id'].toString(),
                    'check'
                  )
                "
              >
                <i class="bi bi-trash"></i> </a
              >&nbsp; &nbsp; &nbsp;
              <a
                :hidden="hiddeEditBtn"
                href="#"
                title="Изменить"
                @click="
                  storeProfile.dataProfile.openForm(
                    'check',
                    'update',
                    props.item['id'].toString(),
                    props.item
                  )
                "
              >
                <i class="bi bi-pencil-square"></i>
              </a>
            </template>
          </RowDivSlot>
          <RowDivSlot
            :label="'Проверка по местам работы<'"
            :value="props.item['workplace']"
          />
          <RowDivSlot :label="'Бывший работник МТСБ'" :value="props.item['employee']" />
          <RowDivSlot :label="'Проверка паспорта'" :value="props.item['document']" />
          <RowDivSlot :label="'Проверка ИНН'" :value="props.item['inn']" />
          <RowDivSlot :label="'Проверка ФССП'" :value="props.item['debt']" />
          <RowDivSlot
            :label="'Проверка банкротства'"
            :value="props.item['bankruptcy']"
          />
          <RowDivSlot :label="'Проверка БКИ'" :value="props.item['bki']" />
          <RowDivSlot :label="'Проверка судебных дел'" :value="props.item['courts']" />
          <RowDivSlot
            :label="'Проверка аффилированности'"
            :value="props.item['affiliation']"
          />
          <RowDivSlot
            :label="'Проверка по списку террористов'"
            :value="props.item['terrorist']"
          />
          <RowDivSlot
            :label="'Проверка нахождения в розыске'"
            :value="props.item['mvd']"
          />
          <RowDivSlot
            :label="'Проверка в открытых источниках'"
            :value="props.item['internet']"
          />
          <RowDivSlot :label="'Проверка Кронос'" :value="props.item['cronos']" />
          <RowDivSlot :label="'Проверка Крос'" :value="props.item['cros']" />
          <RowDivSlot
            :label="'Дополнительная информация'"
            :value="props.item['addition']"
          />
          <RowDivSlot :label="'ПФО'" :value="props.item['pfo']" />
          <RowDivSlot :label="'Комментарии'" :value="props.item['comments']" />
          <RowDivSlot :label="'Результат проверки'" :value="props.item['conclusion']" />
          <RowDivSlot :label="'Сотрудник'" :value="props.item['officer']" />
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
                storeProfile.dataProfile.submitFile(
                  $event,
                  'check',
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
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="storeProfile.dataProfile.openForm('check', 'create')"
          >Добавить запись
        </a>
      </div>
      <RobotDiv />
    </div>
  </div>
</template>
