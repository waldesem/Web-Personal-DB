<script setup lang="ts">
import type { Previous } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Фамилия" name="surname" required>
      <UInput
        v-model.trim.lazy="form.surname"
        placeholder="Фамилия"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput
        v-model.trim.lazy="form.firstname"
        placeholder="Имя"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput
        v-model.trim.lazy="form.patronymic"
        placeholder="Отчество"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Год изменения" name="changed">
      <UInput
        v-model.trim.lazy="form.changed"
        placeholder="Год изменения"
        pattern="^[0-9]{4}$"
      />
    </UFormField>
    <UFormField label="Причина изменения" name="reason">
      <UInput
        v-model.trim.lazy="form.reason"
        placeholder="Причина изменения"
        maxlength="255"
      />
    </UFormField>
    <ElementSubmitButton />
  </UForm>
</template>
