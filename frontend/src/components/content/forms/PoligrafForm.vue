<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Pfo } from "@/interfaces/interface";

const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectArray = defineAsyncComponent(
  () => import("@components/content/elements/SelectArray.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
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

const poligrafForm = toRef(props.poligraf as Pfo);
</script>

<template>
  <form
    @submit.prevent="emit('submit', poligrafForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'ема проверки'">
      <SelectArray
        :name="'theme'"
        :select="[
          'Проверка кандидата', 'Служебная проверка', 'Служебное расследование'
          ]"
        v-model="poligrafForm['theme']"
      />
    </LabelSlot>
    <LabelSlot :label="'Результат'">
      <TextArea
        :name="'results'"
        :place="'Результат'"
        v-model="props.poligraf['results']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
