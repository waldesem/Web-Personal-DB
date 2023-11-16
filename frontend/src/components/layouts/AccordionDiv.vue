<script setup lang="ts">

const props = defineProps({
  id: {
    required: true,
    type: String
  },
  visible: Boolean,
  tables: Array<Object>
});

</script>

<template>
  <div class="accordion" :id="props.id" v-if="props.visible">
    <div class="accordion-item" v-for="tbl, idx in props.tables" :key="idx">
      <h6 class="accordion-header">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" 
                :class="idx !== 0 ? 'collapsed' : ''" 
                :data-bs-target="`#${props.id}${tbl['id' as keyof typeof tbl]}`">
          {{ `ID #${tbl['id' as keyof typeof tbl]}` }}
        </button>
      </h6>
      <div class="accordion-collapse collapse" 
           :class="idx === 0 ? 'show' : ''" 
           :id="props.id + tbl['id' as keyof typeof tbl]" 
           :data-bs-parent="`#${props.id}`">
        <div class="accordion-body">
          <slot mame="body-accordion"></slot>
        </div>
      </div>
    </div>
  </div>
</template>