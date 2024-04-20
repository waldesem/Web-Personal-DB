<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { authStore } from "@store/auth";
import { server } from "@/utilities";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const storeAuth = authStore();

const gptData = ref({
  query: "",
  answer: "",
});

async function getGptAnswers(): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.post(
      `${server}/gpt`, {"query": gptData.value.query}
    );
    const { answer } = response.data;
    gptData.value.answer = answer;
    router.push({ name: "gpt" });
  } catch (error) {
    console.error(error);
  }
}
</script>

<template>
  <div class="row mb-5">
    <HeaderDiv :title="'PrivateGPT'" />
  </div>
  <form @submit.prevent="getGptAnswers"
    class="form-inline" 
    role="search"
  >
    <div class="row mb-3">
      <div class="col-md-11">
        <input 
          type="text"
          name="query"
          class="form-control me-2" 
          placeholder="PrivateGPT"
          v-model="gptData.query"
        >
      </div>
      <div class="col-md-1">
        <button 
          class="btn btn-outline-primary" 
          type="submit"
        >
          <i class="bi bi-search"></i>
        </button>
      </div>
    </div>
  </form>
  <div class="row p-3 font-monospace text-secondary overflow-auto">
    {{ gptData.answer }}
  </div>
</template>