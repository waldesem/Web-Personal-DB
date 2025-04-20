<script setup lang="ts">
import type { Affilation } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {} as Affilation,
  },
});

const affilForm = ref(props.affils as Affilation);
</script>

<template>
  <UForm :state="affilForm" @submit.prevent="emit('update', affilForm)">
    <UFormField class="mb-3" label="Тип участия" name="view" required>
      <USelect
        v-model.trim.lazy="affilForm.view"
        required
        :options="[
          'Являлся государственным/муниципальным служащим',
          'Являлся государственным должностным лицом',
          'Связанные лица работают в государственных организациях',
          'Участвует в деятельности коммерческих организаций',
        ]"
      />
    </UFormField>
    <UFormField class="mb-3" label="Организация" name="organization" required>
      <UInput
        v-model.trim.lazy="affilForm.organization"
        required
        placeholder="Организация"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="ИНН" name="inn">
      <UInput
        v-model.trim.lazy="affilForm.inn"
        placeholder="ИНН"
        maxlength="12"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
