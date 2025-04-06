<script setup lang="ts">
import type { Persons } from "@/types";

const emit = defineEmits(["open"]);

const props = defineProps({
  person: {
    type: Object as () => Persons,
    default: {} as Persons,
  },
});

const loading = ref(false);

const open = () => {
  loading.value = true;
  emit("open", props.person);
  loading.value = false;
};
</script>

<template>
  <ElementsLabelSlot :label="'Фамилия'">
    {{ props.person.surname }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Имя'">
    {{ props.person.firstname }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Отчество'">
    {{ props.person.patronymic }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Дата рождения'">
    {{ new Date(props.person.birthday).toLocaleDateString("ru-RU") }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.birthplace" :label="'Место рождения'">
    {{ props.person.birthplace }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.citizenship" :label="'Гражданство'">
    {{ props.person.citizenship }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.dual" :label="'Двойное гражданство'">
    {{ props.person.dual }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.snils" :label="'СНИЛС'">
    {{ props.person.snils }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.inn" :label="'ИНН'">
    {{ props.person.inn }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.marital" :label="'Семейное положение'">
    {{ props.person.marital }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Дата записи'">
    {{ new Date(props.person.created).toLocaleString("ru-RU") }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.person.addition"
    :label="'Дополнительная информация'"
  >
    {{ props.person.addition }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Материалы'">
    <div class="flex items-center space-x-4">
      <UButton
        :loading="loading"
        label="Открыть"
        variant="outline"
        @click="open"
      />
      <div v-if="props.person.destination">
        {{ props.person.destination }}
      </div>
    </div>
  </ElementsLabelSlot>
</template>
