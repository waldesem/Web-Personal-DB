<script setup lang="ts">

import { messageStore } from '@/store/messages';
import { timeSince } from '@share/utilities';

const storeMessage = messageStore();

</script>

<template>
<div v-if="storeMessage.messages.length" class="toast-container position-static">
  <div class="toast" role="alert" aria-live="assertive" aria-atomic="true"
          v-for="message in storeMessage.messages" :key="message['id']">
    <div class="toast-header">
      <img src="..." class="rounded me-2" alt="...">
      <strong class="me-auto">Сообщение</strong>
      <small class="text-body-secondary">
        {{ timeSince(message['create']) }}
      </small>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      {{ message['report'] }}
    </div>
  </div>
</div>
</template>