<script setup lang="ts">
import type { Contact } from '@/types';

const props = defineProps<Contact>()
</script>

<template>
    <ElementsLabelValue label="Вид" :value="props.view" />
    <ElementsLabelValue label="Контакт" :value="props.contact" />
</template>
