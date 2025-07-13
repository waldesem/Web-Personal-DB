<script setup lang="ts">
import type { Verification } from '@/types';
import { Conclusions } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    default: () => ({}),
  },
});

const checkForm = toRef(props.item as Verification);

const textAreas = {
  workplace: "Проверка по местам работы",
  document: "Проверка документов",
  debt: "Проверка задолженностей",
  bankruptcy: "Проверка банкротства",
  bki: "Проверка Кредитной истории",
  courts: "Проверка судебных дел",
  affilation: "Проверка аффилированности",
  terrorist: "Проверка в списке террористов",
  internet: "Проверка в открытых источниках",
  cronos: "Проверка в Кронос",
  addition: "Дополнительная информация",
};

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
</script>

<template>
  <UFormField label="Негатива нет">
    <USwitch v-model="noNegative" />
  </UFormField>
  <UForm :state="checkForm" @submit.prevent="emit('update', checkForm)">
    <div v-for="(value, key) in textAreas" :key="key">
      <UFormField :label="value" :name="key">
        <UTextarea
          v-model.trim.lazy="checkForm[key]"
          autoresize
          :placeholder="value"
        />
      </UFormField>
    </div>
    <UFormField label="Результат" name="conclusion" required>
      <USelect
        v-model="checkForm.conclusion"
        :items="Object.values(Conclusions)"
        placeholder="Выберите нужное решение из списка"
        required
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
