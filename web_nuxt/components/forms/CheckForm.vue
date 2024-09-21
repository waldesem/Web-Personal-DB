<script setup lang="ts">
import type { Verification } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["cancel", "close", "update"]);

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
  emit("close");
  authFetch("/api/checks/" + props.candId, {
    method: "POST",
    body: checkForm.value,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  emit("update");
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
        placeholder="Проверка по местам работы"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка документов">
      <UTextarea
        v-model.trim.lazy="checkForm['document']"
        placeholder="Проверка документов"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка ИНН">
      <UTextarea
        v-model.trim.lazy="checkForm['inn']"
        placeholder="Проверка ИНН"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка задолженностей">
      <UTextarea
        v-model.trim.lazy="checkForm['debt']"
        placeholder="Проверка задолженностей"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка банкротства">
      <UTextarea
        v-model.trim.lazy="checkForm['bankruptcy']"
        placeholder="Проверка банкротства"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка Кредитной истории">
      <UTextarea
        v-model.trim.lazy="checkForm['bki']"
        placeholder="Проверка Кредитной истории"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка судебных дел">
      <UTextarea
        v-model.trim.lazy="checkForm['courts']"
        placeholder="Проверка судебных дел"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка аффилированности">
      <UTextarea
        v-model.trim.lazy="checkForm['affilation']"
        placeholder="Проверка аффилированности"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в списке террористов">
      <UTextarea
        v-model.trim.lazy="checkForm['terrorist']"
        placeholder="Проверка в списке террористов"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в розыск">
      <UTextarea
        v-model.trim.lazy="checkForm['mvd']"
        placeholder="Проверка в розыск"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в открытых источниках">
      <UTextarea
        v-model.trim.lazy="checkForm['internet']"
        placeholder="Проверка в открытых источниках"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в Кронос">
      <UTextarea
        v-model.trim.lazy="checkForm['cronos']"
        placeholder="Проверка в Кронос/Крос"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дополнительная информация">
      <UTextarea
        v-model.trim.lazy="checkForm['addition']"
        placeholder="Дополнительная информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Комментарии">
      <UTextarea
        v-model.trim.lazy="checkForm['comment']"
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
