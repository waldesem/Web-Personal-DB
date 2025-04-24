<script setup lang="ts">
import StaffDiv from "@/components/divs/StaffDiv.vue";
import EducateDiv from "@/components/divs/EducateDiv.vue";
import WorkDiv from "@/components/divs/WorkDiv.vue";
import DocumDiv from "@/components/divs/DocumDiv.vue";
import AddressDiv from "@/components/divs/AddressDiv.vue";
import ContactDiv from "@/components/divs/ContactDiv.vue";
import PrevDiv from "@/components/divs/PrevDiv.vue";
import RelateDiv from "@/components/divs/RelateDiv.vue";
import AffilDiv from "@/components/divs/AffilDiv.vue";

await preloadComponents([
  "DivsResumeDiv",
  "DivsPrevDiv",
  "DivsStaffDiv",
  "DivsEducateDiv",
  "DivsWorkDiv",
  "DivsDocumDiv",
  "DivsAddressDiv",
  "DivsContactDiv",
  "DivsRelateDiv",
  "DivsAffilDiv",
]);

const emit = defineEmits(["update"]);
</script>

<template>
  <DivsResumeDiv @update="emit('update')" />
  <div
    v-for="(items, idx) in [
      { component: StaffDiv, label: 'Должности', icon: 'i-heroicons-user' },
      {
        component: EducateDiv,
        label: 'Образование',
        icon: 'i-heroicons-academic-cap',
      },
      {
        component: WorkDiv,
        label: 'Места работы',
        icon: 'i-heroicons-briefcase',
      },
      {
        component: DocumDiv,
        label: 'Документы',
        icon: 'i-heroicons-document-text',
      },
      {
        component: AddressDiv,
        label: 'Адреса',
        icon: 'i-heroicons-home-modern',
      },
      { component: ContactDiv, label: 'Контакты', icon: 'i-heroicons-phone' },
      {
        component: PrevDiv,
        label: 'Изменения имени',
        icon: 'i-heroicons-pencil',
      },
      {
        component: RelateDiv,
        label: 'Связанные лица',
        icon: 'i-heroicons-share',
      },
      {
        component: AffilDiv,
        label: 'Аффилированность',
        icon: 'i-heroicons-user-group',
      },
    ]"
    :key="idx"
  >
    <UCollapsible class="m-2">
      <UButton
        :label="items.label as string"
        :icon="items.icon as string"
        color="neutral"
        variant="subtle"
        trailing-icon="i-lucide-chevron-down"
        block
      />
      <template #content>
        <component :is="items.component" />
      </template>
    </UCollapsible>
  </div>
</template>
