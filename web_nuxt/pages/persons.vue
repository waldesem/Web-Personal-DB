<script setup lang="ts">
import { debounce } from "@/utils/utilities";
import {
  stateAnketa,
  stateClassify,
  statePersons,
  stateUser,
} from "@/state/state";

const anketaState = stateAnketa();
const classifyState = stateClassify();
const personState = statePersons();
const userState = stateUser();

const searchPerson = debounce(async () => {
  await personState.getCandidates();
}, 500);

await personState.getCandidates();
</script>

<template>
  <LayoutsMenu>
    <div
      v-if="
        userState.user.value.role == classifyState.classes.value.roles['user']
      "
      class="relative"
    >
      <div class="absolute inset-y-0 right-0" title="Загрузить json">
        <UFormGroup class="mb-3" size="md">
          <template #label>
            <UIcon
              name="i-heroicons-cloud-arrow-up"
              class="w-8 h-8"
              style="cursor:pointer; color:dodgerblue"
            />
          </template>
          <UInput
            v-show="false"
            type="file"
            accept=".json"
            multiple
            @change="anketaState.submitFile($event, 'persons', '0')"
          />
        </UFormGroup>
      </div>
    </div>
    <ElementsHeaderDiv :div="'py-1'" :header="'КАНДИДАТЫ'" />
    <div class="my-6">
      <UInput
        v-model="personState.persons.value.search"
        placeholder="поиск по фамилии, имени, отчеству, дате рождения, инн"
        size="lg"
        @input.prevent="searchPerson"
      />
    </div>
    <UTable
      :empty-state="{ label: 'Ничего не найдено.' }"
      :columns="[
        { key: 'id', label: '#' },
        { key: 'region', label: 'Регион' },
        { key: 'surname', label: 'Фамилия Имя Отчество' },
        { key: 'birthday', label: 'Дата рождения' },
        { key: 'snils', label: 'СНИЛС' },
        { key: 'inn', label: 'ИНН' },
        { key: 'created', label: 'Обновлено' },
        { key: 'username', label: 'Сотрудник' },
        { key: 'editable', label: 'Статус' },
      ]"
      :rows="personState.persons.value.candidates"
    >
      <template #id-data="{ row }">{{ row.id }}</template>
      <template #region-data="{ row }">{{ row.region }}</template>
      <template #surname-data="{ row }">
        <NuxtLink :to="`/profile/${row.id}`">
          {{
            `${row.surname} ${row.firstname} ${
              row.patronymic ? row.patronymic : ""
            }`
          }}
        </NuxtLink>
      </template>
      <template #birthday-data="{ row }">{{
        new Date(row.birthday).toLocaleDateString()
      }}</template>
      <template #birthplace-data="{ row }">{{
        row.birthplace ? row.birthplace : ""
      }}</template>
      <template #inn-data="{ row }">{{ row.inn }}</template>
      <template #created-data="{ row }">{{
        new Date(row.created).toLocaleDateString()
      }}</template>
      <template #username-data="{ row }">{{
        row.username ? row.username.toString().split(" ")[0] : ""
      }}</template>
      <template #editable-data="{ row }">
        <UChip size="2xl" :color="row.editable ? 'red' : 'green'" />
      </template>
      <template #caption>
        <caption class="caption-bottom text-left">
          <UButton
            variant="link"
            icon="i-heroicons-arrow-path"
            :label="`Обновлено: ${personState.persons.value.updated}`"
            @click="personState.getCandidates()"
          />
        </caption>
      </template>
    </UTable>
    <div
      v-if="personState.persons.value.prev || personState.persons.value.next"
      class="grid place-items-center py-8"
    >
      <UButtonGroup orientation="horizontal">
        <UButton
          :disabled="!personState.persons.value.prev"
          variant="link"
          icon="i-heroicons-chevron-double-left"
          @click="personState.getCandidates(personState.persons.value.page - 1)"
        />
        <UButton
          :disabled="!personState.persons.value.next"
          variant="link"
          icon="i-heroicons-chevron-double-right"
          @click="personState.getCandidates(personState.persons.value.page + 1)"
        />
      </UButtonGroup>
    </div>
  </LayoutsMenu>
</template>
