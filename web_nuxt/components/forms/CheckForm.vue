<script setup lang="ts">
import type { Verification } from "@/types";
import { Conclusions } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    default: () => ({}),
  },
});

const form = toRef(props.item);

// Переключатель для автоматического заполнения полей по умолчанию
const noNegative = ref(false);

watch(noNegative, () => {
  if (noNegative.value) {
    Object.assign(form.value, {
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
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Проверка по местам работы" name="workplace">
      <UTextarea
        v-model.trim.lazy="form.workplace"
        autoresize
        placeholder="Проверка по местам работы"
      />
    </UFormField>
    <UFormField label="Проверка документов" name="document">
      <UTextarea
        v-model.trim.lazy="form.document"
        autoresize
        placeholder="Проверка документов"
      />
    </UFormField>
    <UFormField label="Проверка задолженностей" name="debt">
      <UTextarea
        v-model.trim.lazy="form.debt"
        autoresize
        placeholder="Проверка задолженностей"
      />
    </UFormField>
    <UFormField label="Проверка банкротства" name="bankruptcy">
      <UTextarea
        v-model.trim.lazy="form.bankruptcy"
        autoresize
        placeholder="Проверка банкротства"
      />
    </UFormField>
    <UFormField label="Проверка Кредитной истории" name="bki">
      <UTextarea
        v-model.trim.lazy="form.bki"
        autoresize
        placeholder="Проверка Кредитной истории"
      />
    </UFormField>
    <UFormField label="Проверка судебных дел" name="courts">
      <UTextarea
        v-model.trim.lazy="form.courts"
        autoresize
        placeholder="Проверка судебных дел"
      />
    </UFormField>
    <UFormField label="Проверка аффилированности" name="affilation">
      <UTextarea
        v-model.trim.lazy="form.affilation"
        autoresize
        placeholder="Проверка аффилированности"
      />
    </UFormField>
    <UFormField label="Проверка в списке террористов" name="terrorist">
      <UTextarea
        v-model.trim.lazy="form.terrorist"
        autoresize
        placeholder="Проверка в списке террористов"
      />
    </UFormField>
    <UFormField label="Проверка в открытых источниках" name="internet">
      <UTextarea
        v-model.trim.lazy="form.internet"
        autoresize
        placeholder="Проверка в открытых источниках"
      />
    </UFormField>
    <UFormField label="Проверка в Кронос" name="cronos">
      <UTextarea
        v-model.trim.lazy="form.cronos"
        autoresize
        placeholder="Проверка в Кронос"
      />
    </UFormField>
    <UFormField label="Дополнительная информация" name="addition">
      <UTextarea
        v-model.trim.lazy="form.addition"
        autoresize
        placeholder="Дополнительная информация"
      />
    </UFormField>
    <UFormField label="Результат" name="conclusion" required>
      <USelect
        v-model="form.conclusion"
        :items="Object.values(Conclusions)"
        placeholder="Выберите нужное решение из списка"
        required
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
