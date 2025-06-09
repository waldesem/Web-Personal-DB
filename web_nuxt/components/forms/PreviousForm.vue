<script setup lang="ts">
const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    default: () => ({}),
  },
});

const previousForm = toRef(props.item as Previous);
</script>

<template>
  <UForm :state="previousForm" @submit.prevent="emit('update', previousForm)">
    <UFormField label="Фамилия" name="surname" required>
      <UInput
        v-model.trim.lazy="previousForm.surname"
        placeholder="Фамилия"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput
        v-model.trim.lazy="previousForm.firstname"
        placeholder="Имя"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput
        v-model.trim.lazy="previousForm.patronymic"
        placeholder="Отчество"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Год изменения" name="changed">
      <UInput
        v-model.trim.lazy="previousForm.changed"
        placeholder="Год изменения"
        maxlength="4"
      />
    </UFormField>
    <UFormField label="Причина изменения" name="reason">
      <UInput
        v-model.trim.lazy="previousForm.reason"
        placeholder="Причина изменения"
        maxlength="255"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
