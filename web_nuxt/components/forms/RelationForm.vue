<script setup lang="ts">
import type { Relation } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["cancel", "close", "update"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {} as Relation,
  },
  candId: {
    type: String,
    default: "",
  },
});

const relationForm = toRef(props.relation as Relation);

async function submitRelation() {
  emit("close");
  await authFetch("/api/relations/" + props.candId, {
    method: "POST",
    body: relationForm.value,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  emit("update");
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(relationForm.value, {
    relation: "",
    relation_id: "",
  } as Relation);
}
</script>

<template>
  <UForm :state="relationForm" @submit.prevent="submitRelation">
    <UFormGroup class="mb-3" label="Тип связи">
      <USelect
        v-model.trim.lazy="relationForm['relation']"
        required
        :options="[
          'Одно лицо',
          'Родители-Дети',
          'Братья-Сестры',
          'Супруг-Супруга',
          'Родственники',
          'Близкая связь',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ID связи">
      <UInput
        v-model.trim.lazy="relationForm['relation_id']"
        required
        type="number"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
