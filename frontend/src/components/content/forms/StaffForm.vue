<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Staff } from "@/interfaces/interface";

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
  staff: {
    type: Object as () => Staff,
    default: {},
  },
});

const staffForm = computed(() => {
  return props.staff as Staff;
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', staffForm)"
    class="form form-check"
    role="form"
  >
    <InputElement
      :name="'position'"
      :label="'Должность'"
      :need="true"
      v-model="staffForm['position']"
    />
    <InputElement
      :name="'department'"
      :label="'Подразделение'"
      v-model="staffForm['department']"
    />
    <BtnGroup>
      <BtnGroupContent/>
    </BtnGroup>
  </form>
</template>
