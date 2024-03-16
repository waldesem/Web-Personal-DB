<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Work } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
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
    <TextLabel
      :name="'address'"
      :label="'Адрес организации'"
      v-model="workForm['address']"
    />
    <TextLabel
      :name="'position'"
      :label="'Должность'"
      v-model="workForm['position']"
    />
    <TextLabel
      :name="'reason'"
      :label="'Причина увольнения'"
      v-model="workForm['reason']"
    />
    <BtnGroup>
      <button
        class="btn btn-outline-primary btn-md"
        data-bs-dismiss="modal"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      <button 
        class="btn btn-outline-secondary btn-md" 
        name="reset" 
        type="reset"
      >
        Очистить
      </button>
    </BtnGroup>
  </form>
</template>
