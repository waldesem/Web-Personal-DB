<script setup lang="ts">
import { ref, toRef, watch } from "vue";
import { stateClassify, stateAnketa } from "@/utils/state";
import type { Verification } from "@/utils/interfaces";

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
      <ElementsLabelSlot :label="'Негатива нет'">
        <ElementsSwitchBox
          :name="'noNegative'"
          v-model="noNegative"
        />
      </ElementsLabelSlot>
    </form>
    <form
      @submit.prevent="submitCheck"
      class="form form-check"
      role="form"
      id="checkFormId"
    >
      <ElementsLabelSlot :label="'Проверка по местам работы'">
        <ElementsTextArea
          :name="'workplace'"
          :place="'Проверка по местам работы'"
          v-model="checkForm['workplace']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка документов'">
        <ElementsTextArea
          :name="'document'"
          :place="'Проверка документов'"
          v-model="checkForm['document']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка ИНН'">
        <ElementsTextArea
          :name="'inn'"
          :place="'Проверка ИНН'"
          v-model="checkForm['inn']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка задолженностей'">
        <ElementsTextArea
          :name="'debt'"
          :place="'Проверка задолженностей'"
          v-model="checkForm['debt']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка решений о признании банкротом'">
        <ElementsTextArea
          :name="'bankruptcy'"
          :place="'Проверка решений о признании банкротом'"
          v-model="checkForm['bankruptcy']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка кредитной истории'">
        <ElementsTextArea
          :name="'bki'"
          :place="'Проверка кредитной истории'"
          v-model="checkForm['bki']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка судебных дел'">
        <ElementsTextArea
          :name="'courts'"
          :place="'Проверка судебных дел'"
          v-model="checkForm['courts']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка аффилированности'">
        <ElementsTextArea
          :name="'affilation'"
          :place="'Проверка аффилированности'"
          v-model="checkForm['affilation']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка в списке террористов'">
        <ElementsTextArea
          :name="'terrorist'"
          :place="'Проверка в списке террористов'"
          v-model="checkForm['terrorist']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка в розыск'">
        <ElementsTextArea
          :name="'mvd'"
          :place="'Проверка в розыск'"
          v-model="checkForm['mvd']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка в открытых источниках'">
        <ElementsTextArea
          :name="'internet'"
          :place="'Проверка в открытых источниках'"
          v-model="checkForm['internet']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка в Кронос'">
        <ElementsTextArea
          :name="'cronos'"
          :place="'Проверка в Кронос'"
          v-model="checkForm['cronos']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Проверка в Крос'">
        <ElementsTextArea
          :name="'cros'"
          :place="'Проверка в Крос'"
          v-model="checkForm['cros']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Комментарии'">
        <ElementsTextArea
          :name="'comments'"
          :place="'Комментарий'"
          v-model="checkForm['comment']"
        ></ElementsTextArea>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Результат'">
        <ElementsSelectDiv
          :name="'conclusion'"
          :need="true"
          :select="stateClassify.classes.conclusions"
          v-model="checkForm['conclusion']"
        />
      </ElementsLabelSlot>
      <ElementsBtnGroup @cancel="emit('cancel')"/>
    </form>
  </div>
</template>
