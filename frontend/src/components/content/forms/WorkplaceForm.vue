<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Work } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/InputLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/BtnGroupContent.vue")
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
    <InputLabel
      :name="'start_date'"
      :label="'Начало работы'"
      :typeof="'date'"
      v-model="workForm['start_date']"
    />
    <InputLabel
      :name="'end_date'"
      :label="'Окончание работы'"
      :typeof="'date'"
      v-model="workForm['end_date']"
    />
    <InputLabel
      :name="'workplace'"
      :label="'Место работы'"
      :need="true"
      v-model="workForm['workplace']"
    />
    <InputLabel
      :name="'position'"
      :label="'Должность'"
      :need="true"
      v-model="workForm['position']"
    />
    <InputLabel
      :name="'address'"
      :label="'Адрес организации'"
      v-model="workForm['address']"
    />
    <InputLabel
      :name="'reason'"
      :label="'Причина увольнения'"
      v-model="workForm['reason']"
    />
    <BtnGroup>
      <BtnGroupContent/>
    </BtnGroup>
  </form>
</template>
