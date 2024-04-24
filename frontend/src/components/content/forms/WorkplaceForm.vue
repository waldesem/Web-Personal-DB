<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Work } from "@/interfaces";
import { clearForm } from "@/utilities";

const SwitchBox = defineAsyncComponent(
  () => import("@components/content/elements/SwitchBox.vue")
);
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
  work: {
    type: Object as () => Work,
    default: {},
  },
});

const workForm = toRef(props.work as Work);
</script>

<template>
  <form
    @submit.prevent="emit('submit', workForm); clearForm(workForm)"
    class="form form-check"
    role="form"
  > 
   <SwitchBox
      :div-class="'offset-lg-2 col-lg-10'"
      :name="'now_work'"
      :place="'Текущая работа'"
      v-model="workForm['now_work']"
    />
    <LabelSlot :label="'Начало работы'">
      <InputElement
        :name="'start_date'"
        :place="'Начало работы'"
        :typeof="'date'"
        v-model="workForm['start_date']"
      />
    </LabelSlot>
    <LabelSlot
      v-if="!workForm['now_work']" 
      :label="'Окончание работы'">
      <InputElement
        :name="'end_date'"
        :place="'Окончание работы'"
        :typeof="'date'"
        v-model="workForm['end_date']"
      />
    </LabelSlot>
    <LabelSlot :label="'Место работы'">
      <InputElement
        :name="'workplace'"
        :place="'Место работы'"
        :need="true"
        v-model="workForm['workplace']"
      />
    </LabelSlot>
    <LabelSlot :label="'Должность'">
      <InputElement
        :name="'position'"
        :place="'Должность'"
        :need="true"
        v-model="workForm['position']"
      />
    </LabelSlot>
    <LabelSlot :label="'Тип занятости'">
      <InputElement
        :name="'address'"
        :place="'Адрес организации'"
        v-model="workForm['address']"
      />
    </LabelSlot>
    <LabelSlot :label="'Причина увольнения'">
      <InputElement
        :name="'reason'"
        :place="'Причина увольнения'"
        v-model="workForm['reason']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent 
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
