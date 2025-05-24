<script setup lang="ts">
import type { Verification } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type:  Object as PropType<Verification>,
    default: () => ({}),
  },
});

const checkForm = toRef(props.item as Verification);

const noNegative = ref(false);

watch(noNegative, () => {
  if (noNegative.value) {
    Object.assign(checkForm.value, {
      workplace: "Негатив по местам работы не выявлен",
      document: "Среди недействительных документов не значится",
      debt: "Задолженности не обнаружены",
      bankruptcy: "Решений о признании банкротом не имеется",
      bki: "Кредитная история положительная",
      courts: "Судебные дела не обнаружены",
      affilation: "Аффилированность не выявлена",
      terrorist: "В списке террористов не обнаружен",
      internet: "В открытых источниках негатив не обнаружен",
      cronos: "В Кронос негатив не выявлен",
    });
  }
});

const textAreas = {
  workplace: ["Проверка по местам работы", checkForm.value.workplace],
  document: ["Проверка документов", checkForm.value.document],
  debt: ["Проверка задолженностей", checkForm.value.debt],
  bankruptcy: ["Проверка банкротства", checkForm.value.bankruptcy],
  bki: ["Проверка Кредитной истории", checkForm.value.bki],
  courts: ["Проверка судебных дел", checkForm.value.courts],
  affilation: ["Проверка аффилированности", checkForm.value.affilation],
  terrorist: ["Проверка в списке террористов", checkForm.value.terrorist],
  internet: ["Проверка в открытых источниках", checkForm.value.internet],
  cronos: ["Проверка в Кронос", checkForm.value.cronos],
  addition: ["Дополнительная информация", checkForm.value.addition],
};
</script>

<template>
  <UFormField label="Негатива нет">
    <USwitch v-model="noNegative" />
  </UFormField>
  <UForm :state="checkForm" @submit.prevent="emit('update', checkForm)">
    <div v-for="(value, key) in textAreas" :key="key">
      <UFormField :label="value[0]" :name="key">
        <UTextarea
          v-model.trim.lazy="checkForm[key]"
          autoresize
          :placeholder="value[0]"
        />
      </UFormField>
    </div>
    <UFormField label="Результат" name="conclusion" required>
      <USelect
        v-model="checkForm.conclusion"
        required
        :items="[
          'СОГЛАСОВАНО',
          'СОГЛАСОВАНО С КОММЕНТАРИЕМ',
          'ОТКАЗАНО В СОГЛАСОВАНИИ',
          'СНЯТ С ПРОВЕРКИ',
        ]"
        placeholder="Выберите нужное решение из списка"
      />
    </UFormField>
    <UButton
        label="Принять"
        color="success"
        variant="outline"
        type="submit"
      />
  </UForm>
</template>
