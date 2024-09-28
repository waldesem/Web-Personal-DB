<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

definePageMeta({
  layout: false,
});

const authFetch = useFetchAuth();

const route = useRoute();

const candId = computed(() => route.params.id) as unknown as string;

const { data: person } = await useAsyncData("anketa", async () => {
  const response = await authFetch('/api/persons/' + candId.value);
  return response as Persons;
});

</script>

<template>
  <div class="p-3">
    <DivsPhotoCard
      :cand-id="candId"
      :destination="person.destination"
    />
    <ElementsHeaderDiv
      :div="'py-3'"
      :header="`${person.surname} ${person.firstname} ${
        person.patronymic ? person.patronymic : ''
      }`"
    />
    <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
      <DivsResumeDiv 
        :cand-id="candId"
        :person="person"/>
    </div>
    <div class="my-3">
      <p class="text-red-800 font-bold p-3">Должности</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsStaffDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Образование</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsEducateDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Места работы</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsWorkDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Документы</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsDocumDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Адреса</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsAddressDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
    <p class="text-red-800 font-bold p-3">Контакты</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsContactDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Аффилированность</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsAffilDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Изменения имени</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsPrevDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Связи</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsRelateDiv :cand-id="candId" />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Проверки кандидата</p>
      <TabsCheckTab :cand-id="candId" />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Проверки на полиграфе</p>
      <TabsPoligrafTab :cand-id="candId" />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Расследования</p>
      <TabsInvestigateTab :cand-id="candId" />
    </div>
    <div class="mt-3">
      <p class="text-red-800 font-bold p-3">Запросы</p>
      <TabsInquiryTab :cand-id="candId" />
    </div>
  </div>
</template>
