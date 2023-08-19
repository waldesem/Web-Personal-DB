<script setup lang="ts">
// компонент для отображения списка кандидатов для пользователя 

import { appAlert } from '@/store/alert';
import TablePersons from '@content/TablePersons.vue'

const alertStore = appAlert();

alertStore.alertAttr = '';
alertStore.alertText = '';

</script>

<template>
    <TablePersons :admin="false" />
</template>