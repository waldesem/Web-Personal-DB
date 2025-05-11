<script setup lang="ts">

async function logout() {
  if (confirm("Вы действительно хотите выйти?")) {
    accessToken.value = "";
    clearNuxtData();
    return navigateTo("/login");
  }
  return;
}
</script>

<template>
  <UContainer>
    <div class="sticky flex items-center justify-between pt-8 pb-16">
      <UTooltip text="На главную страницу">
        <NuxtLink to="/persons">
          <div class="inline-flex flex items-center text-xl font-bold">
            <h3 class="text-blue-600">STAFFSEC</h3>
            &nbsp;
            <h3 class="text-red-600">ФИНТЕХ</h3>
          </div>
        </NuxtLink>
      </UTooltip>
      <div v-if="stateUser.role == 'admin'">
        <UButton 
          icon="i-heroicons-users" 
          to="/users" 
          variant="link"
          label="Пользователи"
        />          
      </div>
      <UTooltip text="Выход">
        <UButton
          class="rounded-full"
          :label="stateUser.username"
          color="error"
          icon="i-heroicons-arrow-left-end-on-rectangle"
          @click="logout()"
        />
      </UTooltip>
    </div>
    <div>
      <slot />
    </div>
  </UContainer>
</template>
