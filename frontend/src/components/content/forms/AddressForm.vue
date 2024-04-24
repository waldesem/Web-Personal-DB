<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Address } from "@/interfaces";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectArray = defineAsyncComponent(
  () => import("@components/content/elements/SelectArray.vue")
);
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {},
  },
});

const addressForm = toRef(props.addrs as Address);
</script>

<template>
  <form
    @submit.prevent="emit('submit', addressForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Вид адреса'">
      <SelectArray
        :name="'view'"
        :select="['Адрес регистрации', 'Адрес проживания', 'Другое']"
        v-model="addressForm['view']"
      />
    </LabelSlot>
    <LabelSlot
      :label="'Адрес'"
    >
      <InputElement
        :name="'address'"
        :place="'Адрес'"
        :need="true"
        v-model="addressForm['address']"
      />
    </LabelSlot>
    <BtnGroup>
      <GroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
