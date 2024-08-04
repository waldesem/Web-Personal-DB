<script setup lang="ts">
import { toRef } from "vue";
import type { Previous } from "../../utils/interfaces";
import { stateAnketa } from "../../utils/state";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  previous: {
    type: Object as () => Previous,
    default: {},
  },
});

const previousForm = toRef(props.previous as Previous);

function submitPrevious() {
  stateAnketa.updateItem("previous", previousForm.value)
  emit('cancel');
  Object.keys(previousForm.value).forEach(
    (key) => delete previousForm.value[key as keyof typeof previousForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitPrevious"
    class="form form-check"
    role="form"
  >
    <ElementsLabelSlot :label="'Фамилия'">
      <ElementsInputElement
          :need="true"
          :name="'surname'"
          :place="'Фамилия*'"
          :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
          v-model="previousForm['surname']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Имя'">
      <ElementsInputElement
        :need="true"
        :name="'firstname'"
        :place="'Имя*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="previousForm['firstname']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Отчество'">
      <ElementsInputElement
        :name="'patronymic'"
        :place="'Отчество'"
        v-model="previousForm['patronymic']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Год изменения'">
      <ElementsInputElement
        :name="'date_change'"
        :place="'Год изменения'"
        v-model="previousForm['changed']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Причина изменения'">
      <ElementsInputElement
        :name="'reason'"
        :place="'Причина изменения'"
        v-model="previousForm['reason']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
