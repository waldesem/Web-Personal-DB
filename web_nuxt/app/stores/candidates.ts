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
  async function getData(per_page: number, search: string) {
    const response = await $api<Candidate[]>("/routes/candidates", {
      query: {
        last_seen_id: data.value.at(-1)?.id ?? null,
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
