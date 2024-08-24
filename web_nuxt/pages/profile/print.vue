<script setup lang="ts">
import { stateAnketa } from "@/state/state";
const anketaState = stateAnketa();
</script>

<template>
  
  <div class="p-3">
    <DivsPhotoCard />
    <div class="py-3">
      <h3 class="text-2xl text-red-800 font-bold">
        {{
          `${anketaState.anketa.value.persons.surname} ${
            anketaState.anketa.value.persons.firstname
          } ${
            anketaState.anketa.value.persons.patronymic
              ? " " + anketaState.anketa.value.persons.patronymic
              : ""
          }`
        }}
      </h3>
    </div>
    <DivsResumeDiv />
    <DivsStaffDiv />
    <DivsEducateDiv />
    <DivsWorkDiv />
    <DivsDocumDiv />
    <DivsAddressDiv />
    <DivsContactDiv />
    <DivsAffilDiv />
    <DivsPrevDiv />
    <DivsRelateDiv />
    <TabsCheckTab />
    <TabsPoligrafTab />
    <TabsInvestigateTab />
    <TabsInquiryTab />
  </div>
</template>