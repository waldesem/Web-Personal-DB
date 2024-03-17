<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
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
          v-for="(item, idx) in props.checks"
          :key="idx"
          :id="'check' + idx"
          :idx="idx.toString()"
          :label="'Проверка #' + (idx + 1)"
        >
          <LabelValue :label="'Действия'">
            <a
              href="#"
              title="Удалить"
              @click="deleteItem(item['id'].toString())"
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
                check.item = item;
                check.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </LabelValue>
          <LabelValue :label="'ID'">{{ item["id"] }}</LabelValue>
          <LabelValue :label="'Проверка по местам работы'">
            {{ item["workplace"] }}
          </LabelValue>
          <LabelValue :label="'Бывший работник МТСБ'">
            {{ item["employee"] }}
          </LabelValue>
          <LabelValue :label="'Проверка паспорта'">
            {{ item["document"] }}
          </LabelValue>
          <LabelValue :label="'Проверка ИНН'">{{ item["inn"] }}</LabelValue>
          <LabelValue :label="'Проверка ФССП'">{{ item["debt"] }}</LabelValue>
          <LabelValue :label="'Проверка банкротства'">
            {{ item["bankruptcy"] }}
          </LabelValue>
          <LabelValue :label="'Проверка БКИ'">{{ item["bki"] }}</LabelValue>
          <LabelValue :label="'Проверка судебных решений'">
            {{ item["courts"] }}
          </LabelValue>
          <LabelValue :label="'Проверка аффилированности'">
            {{ item["affiliation"] }}
          </LabelValue>
          <LabelValue :label="'Проверка по списку террористов'">
            {{ item["terrorist"] }}
          </LabelValue>
          <LabelValue :label="'Проверка в розыск'">{{ item["mvd"] }}</LabelValue>
          <LabelValue :label="'Проверка в открытых источниках'">
            {{ item["internet"] }}
          </LabelValue>
          <LabelValue :label="'Проверка в Кронос'">
            {{ item["cronos"] }}
          </LabelValue>
          <LabelValue :label="'Проверка в Крос'">
            {{ item["cros"] }}
          </LabelValue>
          <LabelValue :label="'Дополнительная информация'">
            {{ item["addition"] }}
          </LabelValue>
          <LabelValue :label="'ПФО'">{{ item["pfo"] }}</LabelValue>
          <LabelValue :label="'Комментарии'">{{ item["comments"] }}</LabelValue>
          <LabelValue :label="'Результат'">{{ item["conclusion"] }}</LabelValue>
          <LabelValue :label="'Сотрудник'">{{ item["officer"] }}</LabelValue>
          <LabelValue :label="'Дата'">
            {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
          </LabelValue>
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
