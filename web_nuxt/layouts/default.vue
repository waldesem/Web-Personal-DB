<script setup lang="ts">
const userState = useUserState();

async function logout() {
  if (!confirm("Вы действительно хотите выйти?")) return;
  accessToken.value = "";
  clearNuxtData();
  clearNuxtState();
  await navigateTo("/login");
}
</script>

<template>
  <UContainer>
    <div class="sticky flex items-center justify-between pt-8 pb-16">
      <UTooltip text="На главную страницу">
        <NuxtLink to="/persons">
          <div class="flex inline-flex items-center text-xl font-bold spase-x-4">
            <h3 class="text-blue-600">STAFFSEC</h3>
            <h3 class="text-red-600">ФИНТЕХ</h3>
          </div> 
        </NuxtLink>
      </UTooltip>
      <div v-if="userState.role == 'admin'">
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
          :label="userState.username"
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
