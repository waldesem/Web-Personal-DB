<script setup lang="ts">
import type { Verification } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  check: {
    type: Object as () => Verification,
    default: {} as Verification,
  },
});

const checkForm = ref(props.check as Verification);

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
  <UFormField class="mb-3" label="Негатива нет">
    <USwitch v-model="noNegative" />
  </UFormField>
  <UForm :state="checkForm" @submit.prevent="emit('update', checkForm)">
    <UFormField class="mb-3" label="Проверка по местам работы" name="workplace">
      <UTextarea
        v-model.trim.lazy="checkForm.workplace"
        autoresize
        placeholder="Проверка по местам работы"
      />
    </UFormField>
    <UFormField class="mb-3" label="Проверка документов" name="document">
      <UTextarea
        v-model.trim.lazy="checkForm.document"
        autoresize
        placeholder="Проверка документов"
      />
    </UFormField>
    <UFormField class="mb-3" label="Проверка задолженностей" name="debt">
      <UTextarea
        v-model.trim.lazy="checkForm.debt"
        autoresize
        placeholder="Проверка задолженностей"
      />
    </UFormField>
    <UFormField class="mb-3" label="Проверка банкротства" name="bankruptcy">
      <UTextarea
        v-model.trim.lazy="checkForm.bankruptcy"
        autoresize
        placeholder="Проверка банкротства"
      />
    </UFormField>
    <UFormField class="mb-3" label="Проверка Кредитной истории" name="bki">
      <UTextarea
        v-model.trim.lazy="checkForm.bki"
        autoresize
        placeholder="Проверка Кредитной истории"
      />
    </UFormField>
    <UFormField class="mb-3" label="Проверка судебных дел" name="courts">
      <UTextarea
        v-model.trim.lazy="checkForm.courts"
        autoresize
        placeholder="Проверка судебных дел"
      />
    </UFormField>
    <UFormField
      class="mb-3"
      label="Проверка аффилированности"
      name="affilation"
    >
      <UTextarea
        v-model.trim.lazy="checkForm.affilation"
        autoresize
        placeholder="Проверка аффилированности"
      />
    </UFormField>
    <UFormField
      class="mb-3"
      label="Проверка в списке террористов"
      name="terrorist"
    >
      <UTextarea
        v-model.trim.lazy="checkForm.terrorist"
        autoresize
        placeholder="Проверка в списке террористов"
      />
    </UFormField>
    <UFormField
      class="mb-3"
      label="Проверка в открытых источниках"
      name="internet"
    >
      <UTextarea
        v-model.trim.lazy="checkForm.internet"
        autoresize
        placeholder="Проверка в открытых источниках"
      />
    </UFormField>
    <UFormField class="mb-3" label="Проверка в Кронос" name="cronos">
      <UTextarea
        v-model.trim.lazy="checkForm.cronos"
        autoresize
        placeholder="Проверка в Кронос/Крос"
      />
    </UFormField>
    <UFormField class="mb-3" label="Дополнительная информация" name="addition">
      <UTextarea
        v-model.trim.lazy="checkForm.addition"
        autoresize
        placeholder="Дополнительная информация"
      />
    </UFormField>
    <UFormField
      v-if="checkForm.conclusion === 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'"
      class="mb-3"
      label="Комментарии"
      name="comment"
    >
      <UTextarea
        v-model.trim="checkForm.comment"
        autoresize
        placeholder="Комментарии"
      />
    </UFormField>
    <UFormField class="mb-3" label="Результат" name="conclusion" required>
      <USelect
        v-model="checkForm.conclusion"
        required
        :items="[
          'СОГЛАСОВАНО',
          'СОГЛАСОВАНО С КОММЕНТАРИЕМ',
          'ОТКАЗАНО В СОГЛАСОВАНИИ',
          'СНЯТ С ПРОВЕРКИ',
        ]"
        placeholder="Выберите решение"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
