<script setup lang="ts">
import type { Affilation } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type:  Object as PropType<Affilation>,
    default: () => ({}),
  },
});

const affilForm = toRef(props.item as Affilation);
</script>

<template>
  <UForm :state="affilForm" @submit.prevent="emit('update', affilForm)">
    <UFormField label="Вид участия" name="view" required>
      <USelect
        v-model="affilForm.view"
        required
        :items="[
          'Являлся государственным/муниципальным служащим',
          'Являлся государственным должностным лицом',
          'Связанные лица работают в государственных организациях',
          'Участвует в деятельности коммерческих организаций',
        ]"
        placeholder="Выберите вид участия"
      />
    </UFormField>
    <UFormField label="Организация" name="organization" required>
      <UInput
        v-model.trim.lazy="affilForm.organization"
        required
        placeholder="Организация"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="ИНН" name="inn">
      <UInput
        v-model.trim.lazy="affilForm.inn"
        placeholder="ИНН"
        maxlength="12"
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
