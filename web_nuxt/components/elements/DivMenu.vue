<script setup lang="ts">
// Компонент для отображения выпадающего списка действий
const props = defineProps({
  labelUpdate: {
    type: String,
    default: "Изменить",
  },
  labelRefresh: {
    type: String,
    default: "Удалить",
  },
  iconUpdate: {
    type: String,
    default: "i-lucide-pencil",
  },
  iconRefresh: {
    type: String,
    default: "i-lucide-trash",
  },
});

const emits = defineEmits(["update", "refresh"]);
</script>

<template>
  <div class="relative">
    <div class="absolute right-0">
      <UDropdownMenu
        :items="[
          {
            label: props.labelUpdate,
            icon: props.iconUpdate,
            onSelect() {
              emits('update');
            },
          },
          {
            label: props.labelRefresh,
            icon: props.iconRefresh,
            onSelect() {
              emits('refresh');
            },
          },
        ]"
        :content="{ align: 'end' }"
      >
        <UButton
          color="neutral"
          icon="i-lucide-ellipsis-vertical"
          variant="ghost"
          title="Выбор действия"
        />
      </UDropdownMenu>
    </div>
  </div>
</template>
