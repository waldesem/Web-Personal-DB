<script setup lang="ts">

const props = defineProps({
  isneed: {
    type: Boolean,
    default: true
  },
  name: String,
  label: String,
  model: {
    type: [String, Number],
    default: ''
  },
  select: Object
});

</script>

<template>
  <div class="mb-3 row">
    <form class="form form-check" role="form">
      <label class="col-form-label col-lg-2" :for="props.name">
        {{props.label}}
      </label>
      <div class="col-lg-10">
        <select class="form-select" 
                :required="props.isneed"
                :id="props.name"
                :name="props.name"
                :value="props.model"
                @input="$emit('input-event', $event)">
          <option v-for="value, key in props.select" :key="key"
                  :value="key">{{value}}</option>
        </select>
      </div>
    </form>
  </div>
</template>