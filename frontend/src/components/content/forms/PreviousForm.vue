<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Previous } from "@/interfaces";
import { clearForm } from "@/utilities";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  previous: {
    type: Object as () => Previous,
    default: {},
  },
});

const previousForm = toRef(props.previous as Previous);
</script>

<template>
  <form
    @submit.prevent="emit('submit', previousForm); clearForm(previousForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Фамилия'">
      <InputElement
          :need="true"
          :name="'surname'"
          :place="'Фамилия*'"
          :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
          v-model="previousForm['surname']"
      />
    </LabelSlot>
    <LabelSlot :label="'Имя'">
      <InputElement
        :need="true"
        :name="'firstname'"
        :place="'Имя*'"
        :pattern="'[А-Яа-яЁё\\-\'\\s]+'"
        v-model="previousForm['firstname']"
      />
    </LabelSlot>
    <LabelSlot :label="'Отчество'">
      <InputElement
        :name="'patronymic'"
        :place="'Отчество'"
        v-model="previousForm['patronymic']"
      />
    </LabelSlot>
    <LabelSlot :label="'Дата изменения'">
      <InputElement
        :name="'date_change'"
        :place="'Год изменения'"
        v-model="previousForm['changed']"
      />
    </LabelSlot>
    <LabelSlot :label="'Причина изменения'">
      <InputElement
        :name="'reason'"
        :place="'Причина изменения'"
        v-model="previousForm['reason']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
