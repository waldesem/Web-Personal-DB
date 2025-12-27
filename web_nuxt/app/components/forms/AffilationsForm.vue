<script setup lang="ts">
import type { Affilation } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Вид участия" name="view" required>
      <USelect
        v-model="form.view"
        :items="[
          'Являлся государственным/муниципальным служащим',
          'Являлся государственным должностным лицом',
          'Связанные лица работают в государственных организациях',
          'Участвует в деятельности коммерческих организаций',
        ]"
        placeholder="Выберите вид участия"
        required
      />
    </UFormField>
    <UFormField label="Организация" name="organization" required>
      <UInput
        v-model.trim.lazy="form.organization"
        placeholder="Организация"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="ИНН" name="inn">
      <UInput v-model.trim.lazy="form.inn" placeholder="ИНН" maxlength="12" />
    </UFormField>
    <ElementSubmitButton />
  </UForm>
</template>
