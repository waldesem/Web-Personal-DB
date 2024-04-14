<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
// import { authStore } from "@store/auth";
// import { server } from "@utilities/utils";
// import { router } from "@/router/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
// const storeAuth = authStore();

const gptData = ref({
  query: "",
  answer: "",
});

async function getGptAnswers(): Promise<void> {
  gptData.value.answer = "Еще не реализовано:-(";
  // try {
  //   const response = await storeAuth.axiosInstance.post(
  //     `${server}/gpt`,
  //     gptData.value.query
  //   );
  //   gptData.value.answer = response.data;
  //   router.push({ name: "gpt" });
  // } catch (error) {
  //   console.error(error);
  // }
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
    <textarea 
      class="form-control me-2" 
      placeholder="PrivateGPT"
      v-model="gptData.query"
    ></textarea>
    <button 
      class="btn btn-outline-primary" 
      type="submit"
    >
      <i class="bi bi-search"></i>
    </button>
  </form>
  <div class="row mb-5 font-monospace text-secondary">{{ gptData.answer }}</div>
</template>