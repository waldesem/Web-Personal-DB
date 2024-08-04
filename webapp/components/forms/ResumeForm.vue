<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "../../utils/state";
import type { Persons } from "../../utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  action: {
    type: String,
    default: "create",
  },
  resume: {
    type: Object as () => Persons,
    default: {},
  },
});

const resumeForm = toRef(props.resume);

function cancelEdit() {
  Object.keys(resumeForm.value).forEach(
    (key) => delete resumeForm.value[key as keyof typeof resumeForm.value]
  );
  emit('cancel')
}

async function submitForm(): Promise<void> {
  stateAnketa.submitResume(props.action, resumeForm.value)
  cancelEdit();
}
</script>

<template>
  <form @submit.prevent="submitForm" class="form form-check" role="form">
    <ElementsLabelSlot :label="'Фамилия'">
      <ElementsInputElement
        :need="true"
        :name="'surname'"
        :place="'Фамилия*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="resumeForm['surname']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Имя'">
      <ElementsInputElement
        :need="true"
        :name="'firstname'"
        :place="'Имя*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="resumeForm['firstname']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Отчество'">
      <ElementsInputElement
        :name="'patronymic'"
        :place="'Отчество'"
        v-model="resumeForm['patronymic']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата рождения*'">
      <ElementsInputElement
        :need="true"
        :name="'birthday'"
        :place="'Дата рождения*'"
        :typeof="'date'"
        v-model="resumeForm['birthday']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Место рождения'">
      <ElementsInputElement
        :name="'birthplace'"
        :place="'Место рождения'"
        v-model="resumeForm['birthplace']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Гражданство'">
      <ElementsInputElement
        :name="'citizenship'"
        :place="'Гражданство'"
        v-model="resumeForm['citizenship']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Двойное гражданство'">
      <ElementsInputElement
        :name="'dual'"
        :place="'Двойное гражданство'"
        v-model="resumeForm['dual']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'СНИЛС'">
      <ElementsInputElement
        :name="'snils'"
        :place="'СНИЛС'"
        :pattern="'[0-9]{11}'"
        v-model="resumeForm['snils']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'ИНН'">
      <ElementsInputElement
        :name="'inn'"
        :place="'ИНН'"
        :max="'12'"
        :pattern="'[0-9]{12}'"
        v-model="resumeForm['inn']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Семейное положение'">
      <ElementsInputElement
        :name="'marital'"
        :place="'Семейное положение'"
        v-model="resumeForm['marital']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дополнительно'">
      <ElementsTextArea
        :name="'addition'"
        :place="'Дополнительно'"
        v-model="resumeForm['addition']"
      ></ElementsTextArea>
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="cancelEdit" />
  </form>
</template>
