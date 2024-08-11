<script setup lang="ts"></script>

<template>
  <LayoutsMenu>
    <div class="py-5">
      <h3 class="text-2xl text-opacity-75 text-red-800 font-bold">
        Создать анкету
      </h3>
    </div>
    <div class="border rounded p-5">
      <FormsResumeForm @cancel="navigateTo('/persons')"/>
    </div>
  </LayoutsMenu>
</template>
