<script setup lang="ts">
import { dataPerson } from "@/composables/personData";

definePageMeta({ layout: false });
</script>

<template>
  <ElementsCardDiv>
    <h3 class="text-2xl font-bold py-1">
      {{
        `${dataPerson.person.surname} ${dataPerson.person.firstname} ${
          dataPerson.person.patronymic ? dataPerson.person.patronymic : ""
        }`
      }}
    </h3>
    <DivsItemsResumeItem :person="dataPerson.person" />

    <h5 v-if="dataPerson.previous" class="text-xl font-bold py-1">Изменения имени</h5>
    <DivsItemsPrevItem
      v-for="item in dataPerson.previous"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.staffs" class="text-xl font-bold py-1">Должности</h5>
    <DivsItemsStaffItem
      v-for="item in dataPerson.staffs"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.documents" class="text-xl font-bold py-1">Документы</h5>
    <DivsItemsDocumItem
      v-for="item in dataPerson.documents"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.educations" class="text-xl font-bold py-1">Образование</h5>
    <DivsItemsEducateItem
      v-for="item in dataPerson.educations"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.workplaces" class="text-xl font-bold py-1">Места работы</h5>
    <DivsItemsWorkItem
      v-for="item in dataPerson.workplaces"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.addresses" class="text-xl font-bold py-1">Адреса</h5>
    <DivsItemsAddressItem
      v-for="item in dataPerson.addresses"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.contacts" class="text-xl font-bold py-1">Контакты</h5>
    <DivsItemsContactItem
      v-for="item in dataPerson.contacts"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.affilations" class="text-xl font-bold py-1">Участие</h5>
    <DivsItemsAffilItem
      v-for="item in dataPerson.affilations"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.checks" class="text-xl font-bold py-1">Проверки</h5>
    <DivsCheckDiv
      v-for="item in dataPerson.checks"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.poligrafs" class="text-xl font-bold py-1">Полиграфы</h5>
    <DivsPoligrafDiv
      v-for="item in dataPerson.poligrafs"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.investigations" class="text-xl font-bold py-1">
      Расследования
    </h5>
    <DivsInvestigateDiv
      v-for="item in dataPerson.investigations"
      :key="item.id"
      :item="item"
    />

    <h5 v-if="dataPerson.inquiries" class="text-xl font-bold py-1">Запросы</h5>
    <DivsInquiryDiv
      v-for="item in dataPerson.inquiries"
      :key="item.id"
      :item="item"
    />
  </ElementsCardDiv>
</template>
