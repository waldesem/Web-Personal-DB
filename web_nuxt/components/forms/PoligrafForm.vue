<script setup lang="ts">
import type { Pfo } from "@/types/interfaces";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: {} as Pfo,
  },
  candId: {
    type: String,
    default: "",
  },
});

const poligrafForm = toRef(props.poligraf as Pfo);

function submitPoligraf() {
  emit("cancel");
  const response = await authFetch('/api/poligrafs/' + props.candId, {
    method: "POST",
    body: poligrafForm.value,
  });
  console.log(response);
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  emit("update");
  poligrafForm.value.theme = "";
  poligrafForm.value.results = "";
}

function cancelAction() {
  emit("cancel");
  poligrafForm.value.theme = "";
  poligrafForm.value.results = "";
}
</script>

<template>
  <UForm :state="poligrafForm" @submit.prevent="submitPoligraf">
    <UFormGroup class="mb-3" label="Тема проверки">
      <USelect
        v-model="poligrafForm['theme']"
        required
        :options="[
          'Проверка кандидата',
          'Служебная проверка',
          'Служебное расследование',
          'Плановое мероприятие',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Результат">
      <UTextarea
        v-model.trim.lazy="poligrafForm['results']"
        required
        placeholder="Результат"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
