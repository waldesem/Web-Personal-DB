<script setup lang="ts">

import { useRoute } from 'vue-router' ;
import NavbarAdmin from './NavbarAdmin.vue'
import PersonsTable from '../TablePersons.vue'
import FooterDiv from '../FooterDiv.vue';

const route = useRoute();
const path = route.params.flag as string | undefined;

</script>

<template>
    <NavbarAdmin />
    <PersonsTable :flag="path" :admin="true" />
    <FooterDiv />
</template>