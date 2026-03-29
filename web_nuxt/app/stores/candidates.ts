import type { Candidate } from "@/types";

export const useCandidateStore = defineStore("candidates", () => {
  const { $api } = useNuxtApp();

  const data = ref({} as Candidate[]);

  const updated = ref(Date.now()); // Дата обновления данных

  // Вычисляем количество страниц
  const total = computed(() => {
    return data.value[0]?.total ?? 1;
  });

  const lastId = computed(() => {
    return data.value.at(-1)?.id ?? null;
  });

  // Определяем функцию для получения данных из API
  async function getData(per_page: number, search: string) {
    try {
      const response = await $api<Candidate[]>("/routes/candidates", {
        query: {
          last_seen_id: lastId.value,
          per_page: per_page,
          search: search,
        },
      });
      updated.value = Date.now();
      return response;
    } catch (error) {
      console.error(error);
    }
  }

  return {
    data,
    updated,
    total,
    getData,
  };
});
