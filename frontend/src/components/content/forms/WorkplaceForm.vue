<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Work } from "@/interfaces/interface";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroupContent.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  work: {
    type: Object as () => Work,
    default: {},
  },
});

const workForm = computed(() => {
  return props.work as Work;
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', workForm)"
    class="form form-check"
    role="form"
  >
    <InputElement
      :name="'start_date'"
      :label="'Начало работы'"
      :typeof="'date'"
      v-model="workForm['start_date']"
    />
    <InputElement
      :name="'end_date'"
      :label="'Окончание работы'"
      :typeof="'date'"
      v-model="workForm['end_date']"
    />
    <InputElement
      :name="'workplace'"
      :label="'Место работы'"
      :need="true"
      v-model="workForm['workplace']"
    />
    <InputElement
      :name="'position'"
      :label="'Должность'"
      :need="true"
      v-model="workForm['position']"
    />
    <InputElement
      :name="'address'"
      :label="'Адрес организации'"
      v-model="workForm['address']"
    />
    <InputElement
      :name="'reason'"
      :label="'Причина увольнения'"
      v-model="workForm['reason']"
    />
    <BtnGroup>
      <BtnGroupContent/>
    </BtnGroup>
  </form>
</template>
