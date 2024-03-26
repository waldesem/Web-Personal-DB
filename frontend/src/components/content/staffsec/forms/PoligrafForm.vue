<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Pfo } from "@/interfaces/interface";

const TextLabel = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/TextLabel.vue")
);
const SelectArray = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/SelectArray.vue")
)
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/BtnGroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: {},
  },
});

const poligrafForm = computed(() => {
  return props.poligraf as Pfo;
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', poligrafForm)"
    class="form form-check"
    role="form"
  >
    <SelectArray
      :name="'theme'"
      :label="'Тема проверки'"
      :select="[
        'Проверка кандидата', 'Служебная проверка', 'Служебное расследование'
        ]"
      v-model="poligrafForm['theme']"
    />
    <TextLabel
      :name="'results'"
      :label="'Результат'"
      v-model="props.poligraf['results']"
    />
    <BtnGroup>
      <BtnGroupContent/>
      <button
        class="btn btn-outline-danger btn-md"
        type="button"
        @click="emit('cancel')"
        name="cancel"
      >
      Отмена
      </button>
    </BtnGroup>
  </form>
</template>
