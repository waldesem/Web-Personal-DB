<script setup lang="ts">
import { z } from "zod";
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

const schema = z.object({
  workplace: z.string().nullable().optional(),
  document: z.string().nullable().optional(),
  inn: z.string().nullable().optional(),
  debt: z.string().nullable().optional(),
  bankruptcy: z.string().nullable().optional(),
  bki: z.string().nullable().optional(),
  courts: z.string().nullable().optional(),
  affilation: z.string().nullable().optional(),
  terrorist: z.string().nullable().optional(),
  mvd: z.string().nullable().optional(),
  internet: z.string().nullable().optional(),
  cronos: z.string().nullable().optional(),
  addition: z.string().nullable().optional(),
  comment: z.string().nullable().optional(),
  conclusion: z.string({ required_error: "Обязательное поле" }),
});

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
  } else {
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
    });
  }
});
</script>

<template>
  <UFormGroup :state="noNegative" class="mb-3" label="Негатива нет">
    <UToggle v-model="noNegative" />
  </UFormGroup>
  <UForm
    :state="checkForm"
    :schema="schema"
    @submit.prevent="emit('update', checkForm)"
  >
    <UFormGroup class="mb-3" label="Проверка по местам работы" name="workplace">
      <UTextarea
        v-model.trim.lazy="checkForm['workplace']"
        autoresize
        placeholder="Проверка по местам работы"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка документов" name="document">
      <UTextarea
        v-model.trim.lazy="checkForm['document']"
        autoresize
        placeholder="Проверка документов"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка ИНН" name="inn">
      <UTextarea
        v-model.trim.lazy="checkForm['inn']"
        autoresize
        placeholder="Проверка ИНН"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка задолженностей" name="debt">
      <UTextarea
        v-model.trim.lazy="checkForm['debt']"
        autoresize
        placeholder="Проверка задолженностей"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка банкротства" name="bankruptcy">
      <UTextarea
        v-model.trim.lazy="checkForm['bankruptcy']"
        autoresize
        placeholder="Проверка банкротства"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка Кредитной истории" name="bki">
      <UTextarea
        v-model.trim.lazy="checkForm['bki']"
        autoresize
        placeholder="Проверка Кредитной истории"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка судебных дел" name="courts">
      <UTextarea
        v-model.trim.lazy="checkForm['courts']"
        autoresize
        placeholder="Проверка судебных дел"
      />
    </UFormGroup>
    <UFormGroup
      class="mb-3"
      label="Проверка аффилированности"
      name="affilation"
    >
      <UTextarea
        v-model.trim.lazy="checkForm['affilation']"
        autoresize
        placeholder="Проверка аффилированности"
      />
    </UFormGroup>
    <UFormGroup
      class="mb-3"
      label="Проверка в списке террористов"
      name="terrorist"
    >
      <UTextarea
        v-model.trim.lazy="checkForm['terrorist']"
        autoresize
        placeholder="Проверка в списке террористов"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в розыск" name="mvd">
      <UTextarea
        v-model.trim.lazy="checkForm['mvd']"
        autoresize
        placeholder="Проверка в розыск"
      />
    </UFormGroup>
    <UFormGroup
      class="mb-3"
      label="Проверка в открытых источниках"
      name="internet"
    >
      <UTextarea
        v-model.trim.lazy="checkForm['internet']"
        autoresize
        placeholder="Проверка в открытых источниках"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Проверка в Кронос" name="cronos">
      <UTextarea
        v-model.trim.lazy="checkForm['cronos']"
        autoresize
        placeholder="Проверка в Кронос/Крос"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дополнительная информация" name="addition">
      <UTextarea
        v-model.trim.lazy="checkForm['addition']"
        autoresize
        placeholder="Дополнительная информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Комментарии" name="comment">
      <UTextarea
        v-model.trim.lazy="checkForm['comment']"
        autoresize
        placeholder="Комментарии"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Результат" name="conclusion" required>
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
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
