<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { classifyStore } from "@/store/classify";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const CheckForm = defineAsyncComponent(() => import("../forms/CheckForm.vue"));
const RobotDiv = defineAsyncComponent(() => import("../divs/RobotDiv.vue"));
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

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
    type: Object as () => Record<any, string>,
    required: true,
  },
  checks: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
  robots: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const check = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
  hideEditBtn:
    props.resume['status_id'] !== storeClassify.classData.status["save"] &&
    props.resume['status_id'] !== storeClassify.classData.status["cancel"] &&
    props.resume['status_id'] !== storeClassify.classData.status["manual"],
});

function cancelEdit() {
  Object.assign(check.value, {
    action: "",
    item: {},
  });
}

function submitForm(form: Object) {
  emit("submit", [check.value.action, "check", check.value.itemId, form]);
  cancelEdit();
}

function submitFile(event: Event) {
  emit("file", event);
}

function deleteItem(itemId: string) {
  emit("delete", [itemId, "check"]);
}

function getRobot() {
  emit("get-item", "robot");
}
</script>

<template>
  <div class="py-3">
    <ModalWin
      :title="check.action === 'update' ? 'Изменить запись' : 'Добавить запись'"
      :id="'modalCheck'"
      @cancel="cancelEdit"
    >
      <CheckForm :content="check.item" @submit="submitForm" />
    </ModalWin>
    <div v-if="props.checks.length > 0 && props.robots.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.checks"
        :key="idx"
        :id="'check' + idx"
        :idx="idx.toString()"
        :label="'Проверка #' + (idx + 1)"
      >
        <LabelSlot>
          <a
            href="#"
            title="Удалить"
            @click="deleteItem(item['id'].toString())"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            :hidden="![
              storeClassify.classData.status['save'],
              storeClassify.classData.status['cancel'],
              storeClassify.classData.status['manual']
            ].includes(props.resume['status_id']) && props.resume['user_id'] !== props.userId"
            href="#"
            title="Изменить"
            data-bs-toggle="modal"
            data-bs-target="#modalCheck"
            @click="
              check.action = 'update';
              check.item = item;
              check.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </LabelSlot>
        <LabelValue
          :label="'Проверка по местам работы<'"
          :value="item['workplace']"
        />
        <LabelValue :label="'Бывший работник МТСБ'" :value="item['employee']" />
        <LabelValue :label="'Проверка паспорта'" :value="item['document']" />
        <LabelValue :label="'Проверка ИНН'" :value="item['inn']" />
        <LabelValue :label="'Проверка ФССП'" :value="item['debt']" />
        <LabelValue
          :label="'Проверка банкротства'"
          :value="item['bankruptcy']"
        />
        <LabelValue :label="'Проверка БКИ'" :value="item['bki']" />
        <LabelValue :label="'Проверка судебных дел'" :value="item['courts']" />
        <LabelValue
          :label="'Проверка аффилированности'"
          :value="item['affiliation']"
        />
        <LabelValue
          :label="'Проверка по списку террористов'"
          :value="item['terrorist']"
        />
        <LabelValue
          :label="'Проверка нахождения в розыске'"
          :value="item['mvd']"
        />
        <LabelValue
          :label="'Проверка в открытых источниках'"
          :value="item['internet']"
        />
        <LabelValue :label="'Проверка Кронос'" :value="item['cronos']" />
        <LabelValue :label="'Проверка Крос'" :value="item['cros']" />
        <LabelValue
          :label="'Дополнительная информация'"
          :value="item['addition']"
        />
        <LabelValue :label="'ПФО'" :value="item['pfo']" />
        <LabelValue :label="'Комментарии'" :value="item['comments']" />
        <LabelValue :label="'Результат проверки'" :value="item['conclusion']" />
        <LabelValue :label="'Сотрудник'" :value="item['officer']" />
        <LabelValue
          :label="'Дата'"
          :value="
            new Date(String(item['deadline'])).toLocaleDateString('ru-RU')
          "
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
        :disabled="![
          storeClassify.classData.status['update'],
          storeClassify.classData.status['save'],
          storeClassify.classData.status['repeat'],
        ].includes(props.resume['status_id']) && props.resume['user_id'] !== props.userId"
        class="btn btn-outline-primary"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#modalCheck"
        @click="check.action = 'create'"
        >Добавить запись
      </button>
    </div>
  </div>
</template>
