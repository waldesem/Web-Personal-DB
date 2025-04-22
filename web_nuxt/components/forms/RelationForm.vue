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
    <UFormField class="mb-3" label="Тип связи" name="type" required>
      <USelect
        v-model="relationForm.type"
        required
        :items="[
          'Одно лицо',
          'Родители-Дети',
          'Братья-Сестры',
          'Супруг-Супруга',
          'Родственники',
          'Родственники',
        ]"
        placeholder="Выберите тип связи"
      />
    </UFormField>
    <UFormField class="mb-3" label="ID связи" name="right_id" required>
      <UInput
        v-model="relationForm.right_id"
        placeholder="Введите ID связи"
        type="number"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
