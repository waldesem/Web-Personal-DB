<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { stateClassify, stateAnketa, stateUser } from "@/state";
import { Verification } from "@/interfaces";

const IconRelative = defineAsyncComponent(
  () => import("@components/content/elements/IconRelative.vue")
);
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

onBeforeMount(async () => {
  await stateAnketa.getItem("check");
  await stateAnketa.getItem("robot");
});

const check = ref({
  action: "",
  itemId: "",
  item: <Verification>{},
  hideEditBtn:
    stateAnketa.anketa.resume["status_id"] !== stateClassify.status["save"] &&
    stateAnketa.anketa.resume["status_id"] !== stateClassify.status["cancel"] &&
    stateAnketa.anketa.resume["status_id"] !== stateClassify.status["manual"],
  showActions: false
});

function submitForm(form: Object) {
  stateAnketa.updateItem(check.value.action, "check", check.value.itemId, form);
  check.value.action = "";
}
</script>

<template>
  <div class="py-3">
    <div class="text-end">
        <IconRelative v-if="check.action !== 'create' && !stateAnketa.share.printPage"
          :title="`Добавить`"
          :icon-class="`bi bi-journal-check fs-1`"
          :hide="
            ![
              stateClassify.status['update'],
              stateClassify.status['save'],
              stateClassify.status['repeat'],
              stateClassify.status['manual'],
            ].includes(stateAnketa.anketa.resume['status_id']) &&
            stateAnketa.anketa.resume['user_id'] != stateUser.userId
          "
          @onclick="check.action = 'create'"
        />
    </div>
    <CheckForm
      v-if="check.action"
      :check="check.item"
      @cancel="check.action = ''"
      @submit="submitForm"
    />
    <div v-else
      @mouseover="check.showActions = true"
      @mouseout="check.showActions = false"
    >
      <div v-if="stateAnketa.anketa.check.length"> 
        <div class="mb-3" v-for="(item, idx) in stateAnketa.anketa.check" :key="idx">
          <div class="card card-body">
            <LabelSlot>
              <ActionIcons v-show="check.showActions"
                @delete="stateAnketa.deleteItem(item['id'].toString(), 'check')"
                @update="check.action = 'update';
                  check.item = item;
                  check.itemId = item['id'].toString();
                "
                :hide="
                  ![
                    stateClassify.status['save'],
                    stateClassify.status['cancel'],
                    stateClassify.status['manual'],
                  ].includes(stateAnketa.anketa.resume['status_id']) &&
                  stateAnketa.anketa.resume['user_id'] !== stateUser.userId
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
            <LabelSlot :label="'ПФО'">{{ item["pfo"] ? "Да" : "Нет" }}</LabelSlot>
            <LabelSlot :label="'Комментарии'">{{ item["comments"] }}</LabelSlot>
            <LabelSlot :label="'Результат'">{{ item["conclusion"] }}</LabelSlot>
            <LabelSlot :label="'Сотрудник'">{{ stateClassify.users[item["user_id"]] }}</LabelSlot>
            <LabelSlot :label="'Дата'">
              {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
            </LabelSlot>
          </div>
        </div>
        <FileForm :accept="'*'" @submit="stateAnketa.submitFile($event, 'check')" />
        <RobotDiv />
      </div>
      <p v-else>Данные отсутствуют</p>
    </div>
  </div>
</template>
