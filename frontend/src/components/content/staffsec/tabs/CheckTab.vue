<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount, computed } from "vue";
import { classifyStore } from "@/store/classify";
import { Resume, Verification, Robot } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
)
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const CheckForm = defineAsyncComponent(() => import("../forms/CheckForm.vue"));
const RobotDiv = defineAsyncComponent(() => import("../divs/RobotDiv.vue"));

const storeClassify = classifyStore();

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(async () => {
  emit("get-item", "check");
  emit("get-item", "robot");
});

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
  resume: {
    type: Object as () => Resume,
    required: true,
  },
  checks: {
    type: Array as () => Array<Verification>,
    default: () => [],
  },
  robots: {
    type: Array as () => Array<Robot>,
    default: () => [],
  },
});

const check = ref({
  action: "",
  itemId: "",
  item: <Verification>{},
  hideEditBtn:
    props.resume["status_id"] !== storeClassify.classData.status["save"] &&
    props.resume["status_id"] !== storeClassify.classData.status["cancel"] &&
    props.resume["status_id"] !== storeClassify.classData.status["manual"],
});

const checkObj = computed(() => {
  return props.checks.map((item) => ({
    id: ["ID", item["id"]],
    work: ["Проверка по местам работы", item["workplace"]],
    employee: ["Бывший работник МТСБ", item["employee"]],
    document: ["Проверка паспорта", item["document"]],
    inn: ["Проверка ИНН", item["inn"]],
    fssp: ["Проверка ФССП", item["debt"]],
    bankruptcy: [
      "Проверка решений о признании банкротом",
      item["bankruptcy"],
    ],
    bki: ["Проверка БКИ", item["bki"]],
    courts: ["Проверка судебных решений", item["courts"]],
    affiliation: ["Проверка аффилированности", item["affiliation"]],
    terrorist: ["Проверка преступного лица", item["terrorist"]],
    mvd: ["Проверка в розыск", item["mvd"]],
    internet: ["Проверка в открытых источниках", item["internet"]],
    cronos: ["Проверка в Кронос", item["cronos"]],
    cros: ["Проверка в Крос", item["cros"]],
    addition: ["Дополнительная информация", item["addition"]],
    pfo: ["ПФО", item["pfo"]],
    comments: ["Комментарии", item["comments"]],
    conclusion: ["Результат", item["conclusion"]],
    officer: ["Сотрудник", item["officer"]],
    date: [
      "Дата проверки",
      new Date(String(item["deadline"])).toLocaleDateString(
        "ru-RU"
      ),
    ],
  }));
});

function submitForm(form: Object) {
  emit("submit", check.value.action, "check", check.value.itemId, form);
  check.value.action = "";
}

function submitFile(event: Event) {
  emit("file", event);
}

function deleteItem(itemId: string) {
  emit("delete", itemId, "check");
}

function getRobot() {
  emit("get-item", "robot");
}
</script>

<template>
  <div class="py-3">
    <CheckForm
      v-if="check.action"
      :check="check.item"
      @submit="submitForm"
      @cancel="check.action = ''"
    />
    <div v-else>
      <div v-if="props.checks.length || props.robots.length">
        <CollapseDiv
          v-for="(item, idx) in checkObj"
          :key="idx"
          :id="'check' + idx"
          :idx="idx.toString()"
          :label="'Проверка #' + (idx + 1)"
        >
          <div class="row mb-3 d-print-none">
            <div class="col-md-3">
              <label class="form-label">Действия</label>
            </div>
            <div class="col-md-9">
              <a
                href="#"
                title="Удалить"
                @click="deleteItem(item.id[1].toString())"
              >
                <i class="bi bi-trash"></i>
              </a>
              <a
                :hidden="
                  ![
                    storeClassify.classData.status['save'],
                    storeClassify.classData.status['cancel'],
                    storeClassify.classData.status['manual'],
                  ].includes(props.resume['status_id']) &&
                  props.resume['user_id'] !== props.userId
                "
                href="#"
                title="Изменить"
                @click="
                  check.action = 'update';
                  check.item = props.checks[idx];
                  check.itemId = item.id[1].toString();
                "
              >
                <i class="bi bi-pencil-square"></i>
              </a>
            </div>
          </div>
          <LabelValue v-for="(value, key) in item" :key="key"
            :label="value[0]"
            :value="value[1]"
          />
        </CollapseDiv>
        <FileForm :accept="'*'" @submit="submitFile" />
        <RobotDiv
          :robots="props.robots"
          @get-item="getRobot"
          @delete="deleteItem"
        />
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <button
          :disabled="
            ![
              storeClassify.classData.status['update'],
              storeClassify.classData.status['save'],
              storeClassify.classData.status['repeat'],
            ].includes(props.resume['status_id']) &&
            props.resume['user_id'] !== props.userId
          "
          class="btn btn-outline-primary"
          type="button"
          @click="check.action = 'create'"
        >
          Добавить запись
        </button>
      </div>
    </div>
  </div>
</template>
