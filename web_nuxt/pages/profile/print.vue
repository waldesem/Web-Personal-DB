<script setup lang="ts">
import { stateAnketa } from "@/state/state";
const anketaState = stateAnketa();
</script>

<template>
  <div class="p-3">
    <DivsPhotoCard />
    <ElementsHeaderDiv 
      :header="
        anketaState.anketa.value.persons.surname + ' ' +
        anketaState.anketa.value.persons.firstname + ' ' +
        anketaState.anketa.value.persons.patronymic
          ? anketaState.anketa.value.persons.patronymic : ''
        "
    />
    <DivsResumeDiv />
    <div class="my-3">
      <p class="text-red-800 font-bold p-3">Должности</p>
      <DivsStaffDiv />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Образование</p>
      <DivsEducateDiv />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Места работы</p>
      <DivsWorkDiv />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Документы</p>
      <DivsDocumDiv />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Адреса</p>
      <DivsAddressDiv />
    </div>
    <div class="mb-3">
    <p class="text-red-800 font-bold p-3">Контакты</p>
      <DivsContactDiv />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Аффилированность</p>
      <DivsAffilDiv />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Изменения имени</p>
      <DivsPrevDiv />
    </div>
    <div class="mb-3">
      <p class="text-red-800 font-bold p-3">Связи</p>
      <DivsRelateDiv />
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
    <div class="-3">
      <p class="text-red-800 font-bold p-3">Запросы</p>
      <TabsInquiryTab />
    </div>
  </div>
</template>