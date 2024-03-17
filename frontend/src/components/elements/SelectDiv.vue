<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  lblClass: {
    type: String,
    default: "col-form-label col-lg-2",
  },
  slcClass: {
    type: String,
    default: "col-lg-10",
  },
  isneed: {
    type: Boolean,
    default: true,
  },
  name: String,
  label: String,
  select: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const emit = defineEmits(["change-event", "input-event"]);
</script>

<template>
  <div class="mb-3 row">
    <label :class="props.lblClass" :for="props.name">
      {{ props.label }}
    </label>
    <div :class="props.slcClass">
      <select
        class="form-select"
        :required="props.isneed"
        :id="props.name"
        :name="props.name"
        v-model="model"
        @change="emit('change-event', $event)"
        @input="emit('input-event', $event)"
      >
        <option
          v-for="key, _ in props.select"
          :key="key"
          :value="key"
        >
          {{ key }}
        </option>
      </select>
    </div>
  </div>
</template>
