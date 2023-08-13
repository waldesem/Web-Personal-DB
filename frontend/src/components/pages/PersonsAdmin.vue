<script setup lang="ts">

import TablePersons from '@content/TablePersons.vue'

const emit = defineEmits(['updateMessage']);

</script>

<template>
    <TablePersons :admin="true" @updateMessage="emit('updateMessage')" />
</template>