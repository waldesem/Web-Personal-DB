<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Pfo } from "@/interfaces/interface";

const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectInput = defineAsyncComponent(
  () => import("@components/content/elements/SelectInput.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
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
    <LabelSlot :label="'ема проверки'">
      <SelectInput
        :name="'theme'"
        :select="[
          'Проверка кандидата', 'Служебная проверка', 'Служебное расследование'
          ]"
        v-model="poligrafForm['theme']"
      />
    </LabelSlot>
    <TextArea
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
