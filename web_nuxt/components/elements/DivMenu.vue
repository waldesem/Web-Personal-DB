<script setup lang="ts">
const emits = defineEmits(["change", "delete"])
</script>

<template>
  <div class="relative">
    <div class="absolute right-">
      <UDropdownMenu
        :items="[
          {
            label: 'Изменить',
            icon: 'i-heroicons-pencil-square',
            onSelect() {
              emits('change');
            },
          },
          {
            label: 'Удалить',
            icon: 'i-heroicons-trash',
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
          icon="i-heroicons-ellipsis-vertical"
          variant="ghost"
          title="Выбор действия"
        />
      </UDropdownMenu>
    </div>
  </div>
</template>
