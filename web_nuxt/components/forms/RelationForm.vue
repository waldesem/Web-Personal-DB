<script setup lang="ts">
import type { Relation } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {} as Relation,
  },
});

const relationForm = ref(props.relation as Relation);
</script>

<template>
  <UForm :state="relationForm" @submit.prevent="emit('update', relationForm)">
    <UFormGroup class="mb-3" label="Тип связи" name="type" required>
      <USelect
        v-model.trim.lazy="relationForm['type']"
        required
        :options="[
          'Одно лицо',
          'Родители-Дети',
          'Братья-Сестры',
          'Супруг-Супруга',
          'Родственники',
          'Близкая связь',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ID связи" name="right_id" required>
      <UInput
        v-model.trim.lazy="relationForm['right_id']"
        required
        type="number"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>