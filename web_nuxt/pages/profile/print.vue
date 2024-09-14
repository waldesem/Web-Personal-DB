<script setup lang="ts">
import { stateAnketa } from "@/state/state";
const anketaState = stateAnketa();
</script>

<template>
  <div class="p-3">
    <DivsPhotoCard />
    <ElementsHeaderDiv
      :header="`${anketaState.anketa.value.persons.surname} ${
        anketaState.anketa.value.persons.firstname
      } ${
        anketaState.anketa.value.persons.patronymic
          ? anketaState.anketa.value.persons.patronymic
          : ''
      }`"
    />
    <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
      <DivsResumeDiv />
    </div>
    <div class="my-3">
      <p class="text-red-800 font-bold p-3">Должности</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsStaffDiv />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Образование</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsEducateDiv />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Места работы</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsWorkDiv />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Документы</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsDocumDiv />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Адреса</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsAddressDiv />
      </div>
    </div>
    <div class="mb-3">
    <p class="text-red-800 font-bold p-3">Контакты</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsContactDiv />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Аффилированность</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsAffilDiv />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Изменения имени</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsPrevDiv />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Связи</p>
      <div class="text-sm text-gray-500 dark:text-gray-400 py-1">
        <DivsRelateDiv />
      </div>
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Проверки кандидата</p>
      <TabsCheckTab />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Проверки на полиграфе</p>
      <TabsPoligrafTab />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Расследования</p>
      <TabsInvestigateTab />
    </div>
    <div class="mt-3">
      <p class="text-red-800 font-bold p-3">Запросы</p>
      <TabsInquiryTab />
    </div>
  </div>
</template>
