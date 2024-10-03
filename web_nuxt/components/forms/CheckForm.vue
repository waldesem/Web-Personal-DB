<script setup lang="ts">
import type { Verification } from "@/types/interfaces";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  check: {
    type: Object as () => Verification,
    default: {} as Verification,
  },
  candId: {
    type: String,
    default: "",
  },
});

const checkForm = toRef(props.check as Verification);

const noNegative = ref(false);

function submitCheck() {
  emit("update", checkForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  noNegative.value = false;
  Object.keys(checkForm.value).forEach((key) => {
    checkForm.value[key as keyof typeof checkForm.value] = "";
  });
}

watch(noNegative, () => {
  if (noNegative.value) {
    Object.assign(checkForm.value, {
      workplace: "Негатив по местам работы не выявлен",
      document: "Среди недействительных документов не значится",
      inn: "ИНН соответствует",
      debt: "Задолженности не обнаружены",
      bankruptcy: "Решений о признании банкротом не имеется",
      bki: "Кредитная история положительная",
      courts: "Судебные дела не обнаружены",
      affilation: "Аффилированность не выявлена",
      terrorist: "В списке террористов не обнаружен",
      mvd: "В розыск не объявлен",
      internet: "В открытых источниках негатив не обнаружен",
      cronos: "В Кронос негатив не выявлен",
    });
  }
});
</script>

<template>
  <UFormGroup :state="noNegative" class="mb-3" label="Негатива нет">
    <UToggle v-model="noNegative" />
  </UFormGroup>
  <UForm :state="checkForm" @submit.prevent="submitCheck">
    <UFormGroup class="mb-3" label="Проверка по местам работы">
      <UTextarea
        v-model.trim.lazy="checkForm['workplace']"
        autoresize
        placeholder="Проверка по местам работы"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка документов">
      <UTextarea
        v-model.trim.lazy="checkForm['document']"
        autoresize
        placeholder="Проверка документов"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка ИНН">
      <UTextarea
        v-model.trim.lazy="checkForm['inn']"
        autoresize
        placeholder="Проверка ИНН"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка задолженностей">
      <UTextarea
        v-model.trim.lazy="checkForm['debt']"
        autoresize
        placeholder="Проверка задолженностей"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка банкротства">
      <UTextarea
        v-model.trim.lazy="checkForm['bankruptcy']"
        autoresize
        placeholder="Проверка банкротства"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка Кредитной истории">
      <UTextarea
        v-model.trim.lazy="checkForm['bki']"
        autoresize
        placeholder="Проверка Кредитной истории"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка судебных дел">
      <UTextarea
        v-model.trim.lazy="checkForm['courts']"
        autoresize
        placeholder="Проверка судебных дел"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка аффилированности">
      <UTextarea
        v-model.trim.lazy="checkForm['affilation']"
        autoresize
        placeholder="Проверка аффилированности"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в списке террористов">
      <UTextarea
        v-model.trim.lazy="checkForm['terrorist']"
        autoresize
        placeholder="Проверка в списке террористов"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в розыск">
      <UTextarea
        v-model.trim.lazy="checkForm['mvd']"
        autoresize
        placeholder="Проверка в розыск"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в открытых источниках">
      <UTextarea
        v-model.trim.lazy="checkForm['internet']"
        autoresize
        placeholder="Проверка в открытых источниках"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в Кронос">
      <UTextarea
        v-model.trim.lazy="checkForm['cronos']"
        autoresize
        placeholder="Проверка в Кронос/Крос"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дополнительная информация">
      <UTextarea
        v-model.trim.lazy="checkForm['addition']"
        autoresize
        placeholder="Дополнительная информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Комментарии">
      <UTextarea
        v-model.trim.lazy="checkForm['comment']"
        autoresize
        placeholder="Комментарии"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Результат">
      <USelect
        v-model.trim.lazy="checkForm['conclusion']"
        required
        :options="[
          'СОГЛАСОВАНО',
          'СОГЛАСОВАНО С КОММЕНТАРИЕМ',
          'ОТКАЗАНО В СОГЛАСОВАНИИ',
        ]"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
