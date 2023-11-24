<script setup lang="ts">

const props = defineProps({
  need: {
    type: Boolean,
    default: false},
  typeof: {
    type: String,
    default: "text"
  },
  disable: {
    type: Boolean,
    default: false
  },
  place: {
    type: String,
    default: (props: any) => props.label
  },
  pattern: {
    type: String,
    default: '.*'
  },
  max: {
    type: [String, Number],
    default: (props: any) => {
      if (props.typeof === 'text') {
        return '255';
      } else if (props.typeof === 'date') {
        return new Date().toISOString().split('T')[0];
      }
    }
  },
  min: {
    type: String,
    default: '0'
  },
  clsInput: {
    type: String,
    default: 'col-lg-10'
  },
  name: String,
  label: String,
  model: String
});

</script>

<template>
  <div class="mb-3 row">
    <label class="col-form-label col-lg-2" :for="props.name">
      {{ props.label }}
    </label>
    <div :class="props.clsInput">
      <input class="form-control" 
            :disabled="props.disable"
            :max="props.max"
            :min="props.min"
            :id="props.name" 
            :name="props.name"
            :type="props.typeof"
            :required="props.need"
            :pattern="props.pattern"
            :autocomplete="props.name"
            :placeholder="props.label"
            v-model="props.model">
    </div>
  </div>
</template>