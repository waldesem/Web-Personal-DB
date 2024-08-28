<script setup lang="ts">
import { stateAnketa, stateClassify } from "@/state/state";
import type { Verification } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  check: {
    type: Object as () => Verification,
    default: {} as Verification,
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const checkForm = toRef(props.check as Verification);
const noNegative = ref(false);

const selectValues = [
  "Негативной информации не имеется", 
  "Получена значимая информация"
];

// const additionFields = ref({
//   workplace: "",
//     document: "",
//     inn: "",
//     debt: "",
//     bankruptcy: "",
//     bki: "",
//     courts: "",
//     affilation: "",
//     terrorist: "",
//     mvd: "",
//     internet: "",
//     cronos: "",
//     cros: "",
// })

function submitCheck() {
  anketaState.updateItem("checks", checkForm.value)
  noNegative.value = false;
  emit('cancel');
  Object.assign(checkForm.value, {
    workplace: "",
    document: "",
    inn: "",
    debt: "",
    bankruptcy: "",
    bki: "",
    courts: "",
    affilation: "",
    terrorist: "",
    mvd: "",
    internet: "",
    cronos: "",
    cros: "",
    addition: "",
    comment: "",
    conclusion: "",
  } as Verification);
}

const computedWorkplace = computed (() =>  {
  if (additionFields['workplace'] ==  selectValues[0]) {
    return selectValues[0]
  } else {
    return  checkForm['workplace']
  }
});

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
</script>

<template>
  <UForm :state="checkForm" @submit.prevent="submitCheck">
    <UFormGroup class="mb-3" label="Проверка по местам работы">
      <USelectMenu
        v-model="additionField['workplace']"
        :selected="checkForm['workplace'] ? selectValue[1] : selectValue[0]"
        :options="selectValue"
      />
      <UTextarea
v-show="selectValue !== 
        v-model="computedWorkplace"
        placeholder="Проверка по местам работы"
      />
      <!-- <USelect
        v-if="!checkForm['workplace']"
        v-model="additionFields['workplace']"
        :options="['Негатив не выявлен', 'Получена информация']"
      />
      <UTextarea
        v-if="additionFields['workplace'] !== 'Получена информация'"
        v-model="checkForm['workplace']"
        placeholder="Проверка по местам работы"
      /> -->
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка документов">
      <UTextarea
        v-model="checkForm['document']"
        placeholder="Проверка документов"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка ИНН">
      <UTextarea
        v-model="checkForm['inn']"
        placeholder="Проверка ИНН"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка задолженностей">
      <UTextarea
        v-model="checkForm['debt']"
        placeholder="Проверка задолженностей"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка банкротства">
      <UTextarea
        v-model="checkForm['bankruptcy']"
        placeholder="Проверка банкротства"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка Кредитной истории">
      <UTextarea
        v-model="checkForm['bki']"
        placeholder="Проверка Кредитной истории"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка судебных дел">
      <UTextarea
        v-model="checkForm['courts']"
        placeholder="Проверка судебных дел"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка аффилированности">
      <UTextarea
        v-model="checkForm['affilation']"
        placeholder="Проверка аффилированности"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в списке террористов">
      <UTextarea
        v-model="checkForm['terrorist']"
        placeholder="Проверка в списке террористов"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в розыск">
      <UTextarea
        v-model="checkForm['mvd']"
        placeholder="Проверка в розыск"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в открытых источниках">
      <UTextarea
        v-model="checkForm['internet']"
        placeholder="Проверка в открытых источниках"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в Кронос">
      <UTextarea
        v-model="checkForm['cronos']"
        placeholder="Проверка в Кронос/Крос"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дополнительная информация">
      <UTextarea
        v-model="checkForm['addition']"
        placeholder="Дополнительная информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Комментарии">
      <UTextarea
        v-model="checkForm['comment']"
        placeholder="Комментарии"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Результат">
      <USelect
        v-model="checkForm['conclusion']"
        required
        :options="Object.values(classifyState.classes.value.conclusions)"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
