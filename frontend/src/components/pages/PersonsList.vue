<script setup lang="ts">
// компонент для отображения списка кандидатов для пользователя 

import TablePersons from '@content/TablePersons.vue'

const emit = defineEmits(['updateMessage']);

</script>

<template>
    <TablePersons :admin="false" @updateMessage="emit('updateMessage')" />
</template>