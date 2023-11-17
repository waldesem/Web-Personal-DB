<script setup lang="ts">

const props = defineProps({
  has_prev: Boolean,
  has_next: Boolean,
  switchPrev: Promise,
  switchNext: Promise
});

</script>

<template>
    <div class="py-3">
      <nav v-if="has_prev || has_next">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !has_prev }">
            <a class="page-link" href="#" @click="props.switchPrev">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !has_next }">
            <a class="page-link" href="#" @click="props.switchNext">Следующая</a>
          </li>
        </ul>
      </nav>
    </div>
</template>