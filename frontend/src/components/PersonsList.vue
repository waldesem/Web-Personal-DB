<script setup lang="ts">

import NavBar from './NavBar.vue'
import TablePersons from './TablePersons.vue'
import FooterDiv from './FooterDiv.vue';
import { useRoute } from 'vue-router' ;

const route = useRoute();
const flag = route.params.flag as string | undefined;

</script>

<template>
    <NavBar />
    <TablePersons :flag="flag" :admin="false" />
    <FooterDiv />
</template>