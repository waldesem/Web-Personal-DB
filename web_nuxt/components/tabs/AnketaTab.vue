<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

const props = defineProps({
  status: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
  candId: {
    type: String,
    default: "",
  },
  person: {
    type: Object as () => Persons,
    default: {} as Persons,
  },
});

const emit = defineEmits(["update", "message"]);

const items = [
  {
    label: "Резюме",
    icon: "i-heroicons-user",
    defaultOpen: true,
    slot: "resume",
  },
  {
    label: "Должности",
    icon: "i-heroicons-briefcase",
    slot: "staff",
  },
  {
    label: "Образование",
    icon: "i-heroicons-academic-cap",
    slot: "education",
  },
  {
    label: "Работа",
    icon: "i-heroicons-briefcase",
    slot: "work",
  },
  {
    label: "Документы",
    icon: "i-heroicons-document-text",
    slot: "document",
  },
  {
    label: "Адреса",
    icon: "i-heroicons-home-modern",
    slot: "address",
  },
  {
    label: "Контакты",
    icon: "i-heroicons-phone",
    slot: "contact",
  },
  {
    label: "Аффилированные",
    icon: "i-heroicons-user-group",
    slot: "affiliation",
  },
  {
    label: "Изменения имени",
    icon: "i-heroicons-archive-box-arrow-down",
    slot: "prev",
  },
  {
    label: "Связанные",
    icon: "i-heroicons-user-group",
    slot: "relate",
  },
];

function emitMessage(message: string) {
  emit("message", message);
}
</script>

<template>
  <UAccordion :items="items" size="lg" multiple>
    <template #resume="">
      <DivsResumeDiv
        :cand-id="props.candId"
        :editable="props.editable"
        :person="props.person"
        @status='props.props.status"
        @update="emit('update')"
        @message="emitMessage"
      />
    </template>
    <template #staff="">
      <DivsStaffDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
    <template #education="">
      <DivsEducateDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
    <template #work="">
      <DivsWorkDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
    <template #document="">
      <DivsDocumDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
    <template #address="">
      <DivsAddressDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
    <template #contact="">
      <DivsContactDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
    <template #affiliation="">
      <DivsAffilDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
    <template #prev="">
      <DivsPrevDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
    <template #relate="">
      <DivsRelateDiv
        :cand-id="props.candId"
        :editable="props.editable"
        @message="emitMessage"
      />
    </template>
  </UAccordion>
</template>
