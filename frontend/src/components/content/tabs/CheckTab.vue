<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { classifyStore } from "@/store/classify";
import { Anketa, Verification } from "@/interfaces/interface";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const FileForm = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const CheckForm = defineAsyncComponent(
  () => import("@components/content/forms/CheckForm.vue")
);
const RobotDiv = defineAsyncComponent(
  () => import("@components/content/divs/RobotDiv.vue")
);

const storeClassify = classifyStore();

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(() => {
  emit("get-item", "check");
  emit("get-item", "robot");
});

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
  anketa: {
    type: Object as () => Anketa,
    default: {},
  },
});

const check = ref({
  action: "",
  itemId: "",
  item: <Verification>{},
  hideEditBtn:
    props.anketa.resume["status_id"] !== storeClassify.classData.status["save"] &&
    props.anketa.resume["status_id"] !== storeClassify.classData.status["cancel"] &&
    props.anketa.resume["status_id"] !== storeClassify.classData.status["manual"],
  showActions: false
});

function submitForm(form: Object) {
  emit("submit", check.value.action, "check", check.value.itemId, form);
  check.value.action = "";
}

function deleteItem(itemId: string) {
  emit("delete", itemId, "check");
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
    <div v-else
      @mouseover="check.showActions = true"
      @mouseout="check.showActions = false"
    >
      <div v-if="props.anketa.check.length"> 
        <div class="mb-3" v-for="(item, idx) in props.anketa.check" :key="idx">
          <div class="card card-body">
            <LabelSlot>
              <ActionIcons v-show="check.showActions"
                @delete="emit('delete', item['id'].toString(), 'check')"
                @update="check.action = 'update';
                  check.item = item;
                  check.itemId = item['id'].toString();
                "
                :hide="
                  ![
                    storeClassify.classData.status['save'],
                    storeClassify.classData.status['cancel'],
                    storeClassify.classData.status['manual'],
                  ].includes(props.anketa.resume['status_id']) &&
                  props.anketa.resume['user_id'] !== props.userId
                "
              />
            </LabelSlot>
            <LabelSlot :label="'ID'">{{ item["id"] }}</LabelSlot>
            <LabelSlot :label="'Проверка по местам работы'">
              {{ item["workplace"] }}
            </LabelSlot>
            <LabelSlot :label="'Бывший работник МТСБ'">
              {{ item["employee"] }}
            </LabelSlot>
            <LabelSlot :label="'Проверка паспорта'">
              {{ item["document"] }}
            </LabelSlot>
            <LabelSlot :label="'Проверка ИНН'">{{ item["inn"] }}</LabelSlot>
            <LabelSlot :label="'Проверка ФССП'">{{ item["debt"] }}</LabelSlot>
            <LabelSlot :label="'Проверка банкротства'">
              {{ item["bankruptcy"] }}
            </LabelSlot>
            <LabelSlot :label="'Проверка БКИ'">{{ item["bki"] }}</LabelSlot>
            <LabelSlot :label="'Проверка судебных решений'">
              {{ item["courts"] }}
            </LabelSlot>
            <LabelSlot :label="'Проверка аффилированности'">
              {{ item["affiliation"] }}
            </LabelSlot>
            <LabelSlot :label="'Проверка по списку террористов'">
              {{ item["terrorist"] }}
            </LabelSlot>
            <LabelSlot :label="'Проверка в розыск'">{{ item["mvd"] }}</LabelSlot>
            <LabelSlot :label="'Проверка в открытых источниках'">
              {{ item["internet"] }}
            </LabelSlot>
            <LabelSlot :label="'Проверка в Кронос'">
              {{ item["cronos"] }}
            </LabelSlot>
            <LabelSlot :label="'Проверка в Крос'">
              {{ item["cros"] }}
            </LabelSlot>
            <LabelSlot :label="'Дополнительная информация'">
              {{ item["addition"] }}
            </LabelSlot>
            <LabelSlot :label="'ПФО'">{{ item["pfo"] }}</LabelSlot>
            <LabelSlot :label="'Комментарии'">{{ item["comments"] }}</LabelSlot>
            <LabelSlot :label="'Результат'">{{ item["conclusion"] }}</LabelSlot>
            <LabelSlot :label="'Сотрудник'">{{ item["officer"] }}</LabelSlot>
            <LabelSlot :label="'Дата'">
              {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
            </LabelSlot>
          </div>
        </div>
        <FileForm :accept="'*'" @submit="emit('file')" />
        <RobotDiv
          :robots="props.anketa.robot"
          @get-item="emit('get-item', 'robot')"
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
            ].includes(props.anketa.resume['status_id']) &&
            props.anketa.resume['user_id'] !== props.userId
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
