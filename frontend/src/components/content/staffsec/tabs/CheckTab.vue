<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { classifyStore } from "@/store/classify";
import { Verification } from "@/interfaces/interface";
import { Robot } from "@/interfaces/interface";

const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const CheckForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/CheckForm.vue")
);
const RobotDiv = defineAsyncComponent(
  () => import("@components/content/staffsec/tabs/divs/RobotDiv.vue")
);

const storeClassify = classifyStore();

onBeforeMount( async() => {
  await props.getItem("check");
  await props.getItem("robot");
});

const props = defineProps({
  candId: String,
  userId: String,
  checks: {
    type: Array as () => Verification[],
    default: () => {},
  },
  robots: {
    type: Array as () => Robot[],
    default: () => {},
  },
  statusId: {
    type: String,
    required: true,
  },
  getItem: {
    type: Function,
    required: true,
  },
  updateItem: {
    type: Function,
    required: true,
  },
  deleteItem: {
    type: Function,
    required: true,
  },
  submitFile: {
    type: Function,
    required: true,
  },
});

const check = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Verification>{},
  hideEditBtn:
    props.statusId !== storeClassify.classData.status["save"] &&
    props.statusId !== storeClassify.classData.status["cancel"] &&
    props.statusId !== storeClassify.classData.status["manual"],
  hideAddBtn: ![
    storeClassify.classData.status["update"],
    storeClassify.classData.status["save"],
    storeClassify.classData.status["repeat"],
  ].includes(props.statusId),
});
</script>

<template>
  <div class="py-3">
    <template v-if="check.isForm">
      <CheckForm
        :get-item="props.getItem"
        :action="check.action"
        :cand-id="candId"
        :content="check.item"
        :update-item="props.updateItem"
        @deactivate="check.isForm = false; check.action = '';"
      />
    </template>
    <div v-else>
      <div v-if="props.checks.length > 0 && props.robots.length > 0">
        <CollapseDiv
          v-for="(item, idx) in props.checks"
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
                @click="props.deleteItem(item['id'].toString())"
              >
                <i class="bi bi-trash"></i>
              </a>
              <a
                :hidden="check.hideEditBtn"
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
          <RowDivSlot
            :label="'Бывший работник МТСБ'"
            :value="item['employee']"
          />
          <RowDivSlot :label="'Проверка паспорта'" :value="item['document']" />
          <RowDivSlot :label="'Проверка ИНН'" :value="item['inn']" />
          <RowDivSlot :label="'Проверка ФССП'" :value="item['debt']" />
          <RowDivSlot
            :label="'Проверка банкротства'"
            :value="item['bankruptcy']"
          />
          <RowDivSlot :label="'Проверка БКИ'" :value="item['bki']" />
          <RowDivSlot
            :label="'Проверка судебных дел'"
            :value="item['courts']"
          />
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
          <RowDivSlot
            :label="'Результат проверки'"
            :value="item['conclusion']"
          />
          <RowDivSlot :label="'Сотрудник'" :value="item['officer']" />
          <RowDivSlot
            :label="'Дата'"
            :value="
              new Date(String(item['deadline'])).toLocaleDateString('ru-RU')
            "
          />
          <RowDivSlot :slotOne="true" :print="true">
            <form
              class="form"
              enctype="multipart/form-data"
              role="form"
              @change="props.submitFile($event, 'check')"
            >
              <input
                class="form-control"
                id="file"
                type="file"
                ref="file"
                multiple
              />
            </form>
          </RowDivSlot>
        </CollapseDiv>

        <RobotDiv
          :robots="props.robots"
          :get-item="props.getItem"
          :delete-item="props.deleteItem"
        />
      </div>
      <p v-else>Данные отсутствуют</p>
      <BtnGroupForm>
        <div class="d-print-none py-3">
          <a
            :hidden="check.hideAddBtn"
            class="btn btn-outline-primary"
            type="button"
            @click="
              check.isForm = true;
              check.action = 'create';
            "
            >Добавить запись
          </a>
        </div>
      </BtnGroupForm>
    </div>
  </div>
</template>
