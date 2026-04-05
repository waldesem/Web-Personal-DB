import type { Candidate } from "@/types";

export const useCandidateStore = defineStore("candidates", () => {
  const { $api } = useNuxtApp();

  const data = ref([] as Candidate[]);

  const updated = ref(Date.now());

  // Вычисляем количество страниц
  const total = computed(() => {
    return data.value[0]?.total ?? 1;
  });

  // Определяем функцию для получения данных из API
  async function getData(page: number, per_page: number, search: string) {
    const response = await $api<Candidate[]>("/routes/candidates", {
      query: {
        page: page - 1,
        per_page: per_page,
        search: search,
      },
    });
    data.value = response;
    updated.value = Date.now();
  }

  return {
    data,
    total,
    updated,
    getData,
  };
});
