<script setup lang="ts">
import type { Affilation } from "@/types";

const emit = defineEmits(["cancel", "update", 'clear']);

const props = defineProps({
  item: {
    type: Object as () => Affilation,
    default: {} as Affilation,
  },
});

const affilForm = ref(props.item as Affilation);
</script>

<template>
  <UForm :state="affilForm" @submit.prevent="emit('update', affilForm)">
    <UFormField class="mb-3" label="Вид участия" name="view" required>
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
    <ElementsBtnGroup @cancel="emit('cancel')" @clear="emit('clear')" />
  </UForm>
</template>
