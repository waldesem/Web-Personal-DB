<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Relation } from "@/interfaces/interface";

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
  relation: {
    type: Object as () => Relation,
    default: {},
  },
});

const relationForm = computed(() => {
  return props.relation as Relation;
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', relationForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Тип связи'">
      <InputElement
        :name="'relation'"
        :place="'Тип связи'"
        :need="true"
        v-model="relationForm['relation']"
      />
    </LabelSlot>
    <LabelSlot :label="'ID связи'">
      <InputElement
        :name="'relation_id'"
        :place="'ID связи'"
        :need="true"
        v-model="relationForm['relation_id']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
