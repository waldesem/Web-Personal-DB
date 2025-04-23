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
      [StaffDiv, 'Должности', 'i-heroicons-user'],
      [EducateDiv, 'Образование', 'i-heroicons-academic-cap'],
      [WorkDiv, 'Места работы', 'i-heroicons-briefcase'],
      [DocumDiv, 'Документы', 'i-heroicons-document-text'],
      [AddressDiv, 'Адреса', 'i-heroicons-home-modern'],
      [ContactDiv, 'Контакты', 'i-heroicons-phone'],
      [PrevDiv, 'Изменения имени', 'i-heroicons-pencil'],
      [RelateDiv, 'Связанные лица', 'i-heroicons-share'],
      [AffilDiv, 'Аффилированность', 'i-heroicons-user-group'],
    ]"
    :key="idx"
  >
    <UCollapsible class="m-2">
      <UButton
        :label="items[1] as string"
        :icon="items[2] as string"
        color="neutral"
        variant="subtle"
        trailing-icon="i-lucide-chevron-down"
        block
      />
        <template #content>
          <ElementsCardDiv>
            <component :is="items[0]" />
          </ElementsCardDiv>
        </template>
    </UCollapsible>
  </div>
</template>
