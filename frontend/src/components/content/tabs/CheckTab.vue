<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { stateClassify, stateAnketa, stateUser } from "@/state";
import { Verification } from "@/interfaces";

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

onBeforeMount(async () => {
  await stateAnketa.getItem("check");
});

const emit = defineEmits(["cancel"]);

const props = defineProps({
  tabAction: {
    type: String,
    default: "",
  },
  currentTab: {
    type: String,
    default: "",
  }
})

const check = ref({
  itemId: "",
  item: <Verification>{},
  hideEditBtn:
    stateAnketa.anketa.resume["status_id"] !== stateClassify.status["save"] &&
    stateAnketa.anketa.resume["status_id"] !== stateClassify.status["cancel"] &&
    stateAnketa.anketa.resume["status_id"] !== stateClassify.status["manual"],
  showActions: false
});

function submitForm(form: Object, action: string) {
  stateAnketa.updateItem(action, "check", check.value.itemId, form);
  action === "update" ? check.value.itemId = "" : emit("cancel");
}
</script>

<template>
  <CheckForm
    v-if="props.tabAction === 'create' && props.currentTab === 'CheckTab'"
    :action="'create'"
    @cancel="emit('cancel')"
    @submit="submitForm"
  />
  <div v-else-if="stateAnketa.anketa.check.length" class='py-3'> 
    <div
      v-for="(item, idx) in stateAnketa.anketa.check" :key="idx" 
      @mouseover="check.showActions = true"
      @mouseout="check.showActions = false"
      class="card card-body mb-3"
    >
      <CheckForm
        v-if="check.itemId === item['id'].toString()"
        :check="check.item"
        :action="'update'"
        @submit="submitForm"
        @cancel="check.itemId = ''"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons v-show="check.showActions"
            :show-form="true"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'check')"
            @update="
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
          >
          <FileForm 
            v-show="check.showActions" 
            :accept="'*'" 
            @submit="stateAnketa.submitFile($event, 'check')" 
          />
        </ActionIcons>
        </LabelSlot>
        <LabelSlot :label="'ID'">{{ item["id"] }}</LabelSlot>
        <LabelSlot :label="'Проверка по местам работы'">
          {{ item["workplace"] }}
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
          {{ item["affilation"] }}
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
        <LabelSlot :label="'Результат'">{{ item["conclusion_id"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ stateClassify.users[item["user_id"]] }}</LabelSlot>
        <LabelSlot :label="'Дата'">
          {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
