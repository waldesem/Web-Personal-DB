<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Work } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  work: {
    type: Object as () => Work,
    default: {} as Work,
  },
});

const anketaState = stateAnketa();

const workForm = toRef(props.work as Work);

function submitWorkplace() {
  anketaState.updateItem("workplaces", workForm.value)
  emit('cancel');
  Object.assign(workForm.value, {
    now_work: false,
    starts: "",
    finished: "",
    workplace: "",
    position: "",
    addresses: "",
    reason: "",
  } as Work);  
}
</script>

<template>
  <UForm :state="workForm" @submit.prevent="submitWorkplace"> 
    <UFormGroup class="mb-3" label="Текущая работа">
      <UCheckbox
        v-model="workForm['now_work']"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Начало работы">
      <UInput
        v-model="workForm['starts']"
        placeholder="Начало работы"
        type="date"
      />
    </UFormGroup>
    <UFormGroup
      v-if="!workForm['now_work']"
      class="mb-3" label="Окончание работы">
      <UInput
        v-model="workForm['finished']"
        placeholder="Окончание работы"
        type="date"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Место работы">
      <UInput
        v-model="workForm['workplace']"
        required
        placeholder="Место работы"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Должность">
      <UInput
        v-model="workForm['position']"
        required
        placeholder="Должность"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Адрес организации">
      <UInput
        v-model="workForm['addresses']"
        placeholder="Адрес организации"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Причина увольнения">
      <UInput
        v-model="workForm['reason']"
        placeholder="Причина увольнения"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
