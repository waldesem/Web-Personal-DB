<script setup lang="ts">

import { ref, watch } from 'vue'
import { onBeforeMount } from 'vue';
import { useRoute } from 'vue-router';
import { loginStore } from '@/store/login';

const NavBar = () => import('@components/layouts/NavBar.vue');
const AlertMessage = () => import('@components/layouts/AlertMessage.vue');
const FooterDiv = () => import('@components/layouts/FooterDiv.vue');
const ChatButton = () => import('@components/layouts/ChatButton.vue');

const route = useRoute();
const storeLogin = loginStore();
const skipLink = ref()

storeLogin.pageIdentity = route.params.group as string;

onBeforeMount(() => {
  storeLogin.getAuth()
});

watch(
  () => route.path,
  () => {
    skipLink.value.focus()
  }
);

</script>

<template>
  <NavBar />
  <AlertMessage />
  <ul class="skip-links">
    <li>
      <a href="#main" ref="skipLink" class="skip-link">
        Вернуться к основному содержимому
      </a>
    </li>
  </ul>
  <router-view></router-view>
  <ChatButton />
  <FooterDiv />
</template>

<style>
.skip-link {
  white-space: nowrap;
  margin: 1em auto;
  top: 0;
  position: fixed;
  left: 50%;
  margin-left: -72px;
  opacity: 0;
}
.skip-link:focus {
  opacity: 1;
  background-color: white;
  padding: 0.5em;
  border: 1px solid black;
}
</style>