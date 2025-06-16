<script setup lang="ts">
const emits = defineEmits(["change", "delete"])
</script>

<template>
  <div class="relative">
    <div class="absolute right-0">
      <UDropdownMenu
        :items="[
          {
            label: 'Изменить',
            icon: 'i-lucide-pencil',
            onSelect() {
              emits('change');
            },
          },
          {
            label: 'Удалить',
            icon: 'i-lucide-trash',
            onSelect() {
              emits('delete');
            },
          },
        ]"
        :content="{ align: 'end' }"
      >
        <UButton
          size="xl"
          color="neutral"
          icon="i-lucide-ellipsis-vertical"
          variant="ghost"
          title="Выбор действия"
        />
      </UDropdownMenu>
    </div>
  </div>
</template>
