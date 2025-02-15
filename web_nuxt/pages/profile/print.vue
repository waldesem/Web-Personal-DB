<script setup lang="ts">
import { dataPerson } from "@/composables/personData";

definePageMeta({ layout: false });
</script>

<template>
  <ElementsCardDiv>
    <DivsResumeDiv :person="dataPerson.person" />
    
    <DivsPrevDiv :previous="dataPerson.previous" />
    <DivsStaffDiv :staffs="dataPerson.staffs" />
    <DivsDocumDiv :documents="dataPerson.documents" />
    <DivsEducateDiv :educations="dataPerson.educations" />
    <DivsWorkDiv :workplaces="dataPerson.workplaces" />
    <DivsAddressDiv :addresses="dataPerson.addresses" />
    <DivsContactDiv :contacts="dataPerson.contacts" />
    <DivsAffilDiv :affils="dataPerson.affilations" />
    <DivsRelateDiv
      :relates="dataPerson.relations"
      :relationships="dataPerson.relationships"
     
    />
    <DivsCheckDiv
      v-for="item in dataPerson.checks"
      :key="item.id"
      :item="item"
     />
    <DivsPoligrafDiv
      v-for="item in dataPerson.poligrafs"
      :key="item.id"
      :item="item"
    />
    <DivsInvestigateDiv
      v-for="item in dataPerson.investigations"
      :key="item.id"
      :item="item"
    />
    <DivsInquiryDiv
      v-for="item in dataPerson.inquiries"
      :key="item.id"
      :item="item"
    />
  </ElementsCardDiv>
</template>
