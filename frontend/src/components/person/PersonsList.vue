<script setup lang="ts">

import TablePersons from './TablePersons.vue'

const emit = defineEmits(['updateMessage']);


function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};

</script>

<template>
    <TablePersons :admin="false" @updateMessage="updateMessage" />
</template>