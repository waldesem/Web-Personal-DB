<script setup lang="ts">
import type { Previous } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  item: {
    type: Object as () => Previous,
    default: {} as Previous,
  },
});

const previousForm = ref(props.item as Previous);
</script>

<template>
  <UForm :state="previousForm" @submit.prevent="emit('update', previousForm)">
    <UFormField class="mb-3" label="Фамилия" name="surname" required>
      <UInput
        v-model.trim.lazy="previousForm.surname"
        required
        placeholder="Фамилия"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Имя" name="firstname" required>
      <UInput
        v-model.trim.lazy="previousForm.firstname"
        required
        placeholder="Имя"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Отчество" name="patronymic">
      <UInput
        v-model.trim.lazy="previousForm.patronymic"
        placeholder="Отчество"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Год изменения" name="changed">
      <UInput
        v-model.trim.lazy="previousForm.changed"
        placeholder="Год изменения"
        maxlength="4"
      />
    </UFormField>
    <UFormField class="mb-3" label="Причина изменения" name="reason">
      <UInput
        v-model.trim.lazy="previousForm.reason"
        placeholder="Причина изменения"
        maxlength="255"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
