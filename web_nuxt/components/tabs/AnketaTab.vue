<script setup lang="ts">
const emit = defineEmits(["update"]);

await preloadComponents(["DivsResumeDiv", "DivsSharedDiv"]);
</script>

<template>
  <DivsResumeDiv @update="emit('update')" />
  <div
    v-for="(items, idx) in [
      { component: 'staffs', label: 'Должности', icon: 'i-heroicons-user' },
      {
        component: 'educations',
        label: 'Образование',
        icon: 'i-heroicons-academic-cap',
      },
      {
        component: 'workplaces',
        label: 'Места работы',
        icon: 'i-heroicons-briefcase',
      },
      {
        component: 'documents',
        label: 'Документы',
        icon: 'i-heroicons-document-text',
      },
      {
        component: 'addresses',
        label: 'Адреса',
        icon: 'i-heroicons-home-modern',
      },
      { component: 'contacts', label: 'Контакты', icon: 'i-heroicons-phone' },
      {
        component: 'previous',
        label: 'Изменения имени',
        icon: 'i-heroicons-pencil',
      },
      {
        component: 'affilations',
        label: 'Аффилированность',
        icon: 'i-heroicons-user-group',
      },
    ]"
    :key="idx"
  >
    <UCollapsible :unmount-on-hide="false" class="m-2">
      <UButton
        :label="items.label as string"
        :icon="items.icon as string"
        color="neutral"
        variant="subtle"
        trailing-icon="i-lucide-chevron-down"
        block
      />
      <template #content>
        <DivsSharedDiv :component="items.component" />
      </template>
    </UCollapsible>
  </div>
</template>
