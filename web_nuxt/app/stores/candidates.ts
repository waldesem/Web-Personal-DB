import type { Candidate } from "@/types";

export const useCandidateStore = defineStore("candidates", () => {
  const { $api } = useNuxtApp();

  const data = ref([] as Candidate[]);

  const updated = ref(Date.now()); // Дата обновления данных

  const search = ref(); // Дата обновления данных

  // Вычисляем количество страниц
  const total = computed(() => {
    return data.value[0]?.total ?? 1;
  });

  // Определяем функцию для получения данных из API
  async function getData(per_page: number) {
    try {
      const response = await $api<Candidate[]>("/routes/candidates", {
        query: {
          last_seen_id: data.value.at(-1)?.id ?? null,
          per_page: per_page,
          search: search.value,
        },
      });
      data.value = response;
      updated.value = Date.now();
    } catch (error) {
      console.error(error);
    }
  }

  return {
    data,
    search,
    total,
    updated,
    getData,
  };
});
