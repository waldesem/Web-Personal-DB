<script setup lang="ts">
import { ref, defineAsyncComponent, toRef, watch } from "vue";
import { stateClassify, stateAnketa } from "@/state";
import { Verification } from "@/interfaces";

const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const SwitchBox = defineAsyncComponent(
  () => import("@components/content/elements/SwitchBox.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  check: {
    type: Object as () => Verification,
    default: {},
  },
});

const checkForm = toRef(props.check as Verification);

const noNegative = ref(false);

function submitCheck() {
  stateAnketa.updateItem("checks", checkForm.value)
  noNegative.value = false;
  emit('cancel');
  Object.keys(checkForm.value).forEach(
    (key) => delete checkForm.value[key as keyof typeof checkForm.value]
  );
}

watch(noNegative, () => {
  if (noNegative.value) {
    Object.assign(checkForm.value, {
      workplace: "Негатива по местам работы не обнаружено",
      document: "Среди недействительных документов не обнаружен",
      inn: "ИНН соответствует паспорту",
      debt: "Задолженности не обнаружены",
      bankruptcy: "Решений о признании банкротом не имеется",
      bki: "Кредитная история не положительная",
      courts: "Судебные дела не обнаружены",
      affilation: "Аффилированность не выявлена",
      terrorist: "В списке террористов не обнаружен",
      mvd: "В розыск не объявлен",
      internet: "В открытых источниках негатив не обнаружен",
      cronos: "В Кронос негатив не выявлен",
      cros: "В Крос негатив не выявлен",
    });
  }
});
</script>

<template>
  <div class="p-3">
    <form class="form form-check" role="form">
      <LabelSlot :label="'Негатива нет'">
        <SwitchBox
          :name="'noNegative'"
          v-model="noNegative"
        />
      </LabelSlot>
    </form>
    <form
      @submit.prevent="submitCheck"
      class="form form-check"
      role="form"
      id="checkFormId"
    >
      <LabelSlot :label="'Проверка по местам работы'">
        <TextArea
          :name="'workplace'"
          :place="'Проверка по местам работы'"
          v-model="checkForm['workplace']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка документов'">
        <TextArea
          :name="'document'"
          :place="'Проверка документов'"
          v-model="checkForm['document']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка ИНН'">
        <TextArea
          :name="'inn'"
          :place="'Проверка ИНН'"
          v-model="checkForm['inn']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка задолженностей'">
        <TextArea
          :name="'debt'"
          :place="'Проверка задолженностей'"
          v-model="checkForm['debt']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка решений о признании банкротом'">
        <TextArea
          :name="'bankruptcy'"
          :place="'Проверка решений о признании банкротом'"
          v-model="checkForm['bankruptcy']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка кредитной истории'">
        <TextArea
          :name="'bki'"
          :place="'Проверка кредитной истории'"
          v-model="checkForm['bki']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка судебных дел'">
        <TextArea
          :name="'courts'"
          :place="'Проверка судебных дел'"
          v-model="checkForm['courts']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка аффилированности'">
        <TextArea
          :name="'affilation'"
          :place="'Проверка аффилированности'"
          v-model="checkForm['affilation']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка в списке террористов'">
        <TextArea
          :name="'terrorist'"
          :place="'Проверка в списке террористов'"
          v-model="checkForm['terrorist']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка в розыск'">
        <TextArea
          :name="'mvd'"
          :place="'Проверка в розыск'"
          v-model="checkForm['mvd']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка в открытых источниках'">
        <TextArea
          :name="'internet'"
          :place="'Проверка в открытых источниках'"
          v-model="checkForm['internet']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка в Кронос'">
        <TextArea
          :name="'cronos'"
          :place="'Проверка в Кронос'"
          v-model="checkForm['cronos']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Проверка в Крос'">
        <TextArea
          :name="'cros'"
          :place="'Проверка в Крос'"
          v-model="checkForm['cros']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Комментарии'">
        <TextArea
          :name="'comments'"
          :place="'Комментарий'"
          v-model="checkForm['comment']"
        ></TextArea>
      </LabelSlot>
      <LabelSlot :label="'Результат'">
        <SelectDiv
          :name="'conclusion'"
          :need="true"
          :select="stateClassify.classes.conclusions"
          v-model="checkForm['conclusion']"
        />
      </LabelSlot>
      <BtnGroup @cancel="emit('cancel')"/>
    </form>
  </div>
</template>
