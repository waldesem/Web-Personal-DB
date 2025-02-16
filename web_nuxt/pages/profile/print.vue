<script setup lang="ts">
definePageMeta({ layout: false });
</script>

<template>
  <div class="p-6">
    <h3 class="text-2xl font-bold py-3">
      {{
        `${statePerson.person.surname} ${statePerson.person.firstname} ${
          statePerson.person.patronymic ? statePerson.person.patronymic : ""
        }`
      }}
    </h3>
    <div class="mb-3">
      <DivsItemsResumeItem :person="statePerson.person" />
    </div>

    <div v-if="statePerson.previous.length" class="text-lg font-bold py-1">
      Изменения имени
    </div>
    <div class="mb-3">
      <DivsItemsPrevItem
        v-for="item in statePerson.previous"
        :key="item.id"
        :item="item"
      />
    </div>

    <div v-if="statePerson.staffs.length" class="text-lg font-bold py-1">Должности</div>
    <div class="mb-3">
      <DivsItemsStaffItem
        v-for="item in statePerson.staffs"
        :key="item.id"
        :item="item"
      />
    </div>

    <div v-if="statePerson.documents.length" class="text-lg font-bold py-1">
      Документы
    </div>
    <div class="mb-3">
      <DivsItemsDocumItem
        v-for="item in statePerson.documents"
        :key="item.id"
        :item="item"
      />
    </div>

    <div v-if="statePerson.educations.length" class="text-lg font-bold py-1">
      Образование
    </div>
    <div class="mb-3">
      <DivsItemsEducateItem
        v-for="item in statePerson.educations"
        :key="item.id"
        :item="item"
      />
    </div>

    <div v-if="statePerson.workplaces.length" class="text-lg font-bold py-1">
      Места работы
    </div>
    <div class="mb-3">
      <DivsItemsWorkItem
        v-for="item in statePerson.workplaces"
        :key="item.id"
        :item="item"
      />
    </div>

    <div v-if="statePerson.addresses.length" class="text-lg font-bold py-1">Адреса</div>
    <div class="mb-3">
      <DivsItemsAddressItem
        v-for="item in statePerson.addresses"
        :key="item.id"
        :item="item"
      />
    </div>

    <div v-if="statePerson.contacts.length" class="text-lg font-bold py-1">
      Контакты
    </div>
    <div class="mb-3">
      <DivsItemsContactItem
        v-for="item in statePerson.contacts"
        :key="item.id"
        :item="item"
      />
    </div>

    <div v-if="statePerson.affilations.length" class="text-lg font-bold py-1">
      Участие
    </div>
    <div class="mb-3">
      <DivsItemsAffilItem
        v-for="item in statePerson.affilations"
        :key="item.id"
        :item="item"
      />
    </div>

    <div class="text-lg font-bold py-1">Проверки</div>
    <div v-if="statePerson.checks.length" class="mb-3">
      <DivsCheckDiv
        v-for="item in statePerson.checks"
        :key="item.id"
        :item="item"
      />
    </div>
    <div v-else class="mb-3">
      <p>Проверки не найдены</p>
    </div>

    <div class="text-lg font-bold py-1">
      Полиграфы
    </div>
    <div v-if="statePerson.poligrafs.length" class="mb-3">
      <DivsPoligrafDiv
        v-for="item in statePerson.poligrafs"
        :key="item.id"
        :item="item"
      />
    </div>
    <div v-else class="mb-3">
      <p>ПФО не проводилось</p>
    </div>

    <div class="text-lg font-bold py-1">
      Расследования
    </div>
    <div v-if="statePerson.investigations.length" class="mb-3">
      <DivsInvestigateDiv
        v-for="item in statePerson.investigations"
        :key="item.id"
        :item="item"
      />
    </div>
    <div v-else class="mb-3">
      <p>Расследования не проводились</p>
    </div>

    <div class="text-lg font-bold py-1">
      Запросы
    </div>
    <div v-if="statePerson.inquiries.length" class="mb-3">
      <DivsInquiryDiv
        v-for="item in statePerson.inquiries"
        :key="item.id"
        :item="item"
      />
    </div>
    <div v-else class="mb-3">
      <p>Запросы не поступали</p>
    </div>
  </div>
</template>
