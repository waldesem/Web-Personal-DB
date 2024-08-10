<script setup lang="ts">
import { onBeforeMount } from "vue";
import { debounce } from "@/utils/utilities";
import {
  stateAlert,
  stateAnketa,
  stateClassify,
  statePersons,
  stateUser,
} from "@/state/state";

const alertState = stateAlert();
const anketaState = stateAnketa();
const classifyState = stateClassify();
const personState = statePersons();
const userState = stateUser();

onBeforeMount(async () => {
  alertState.alertMessage.value.show = false;
  await personState.getCandidates();
});

const searchPerson = debounce(() => {
  personState.getCandidates();
}, 500);

function openProfile(person_id: string) {
  navigateTo(`/profile/${person_id}`);
}
</script>

<template>
  <LayoutsMenu>
    <div class="py-5">
      <h3 class="text-2xl text-opacity-75 text-red-600 font-bold">
        Кандидаты
      </h3>
    </div>
    <div
      v-if="
        userState.user.value.role == classifyState.classes.value.roles['user']
      "
      class="relative"
    >
      <div class="absolute object-right">
        <FormsFileForm
          :accept="'.json'"
          @submit="anketaState.submitFile($event, 'persons', '0')"
        />
      </div>
    </div>
    <UInput 
      v-model="personState.persons.value.search"
      placeholder="поиск по фамилии, имени, отчеству, дате рождения, инн"
      @input="searchPerson"
    />
    <table v-if="personState.persons.value.candidates.length">
      <caption>
        {{ `Обновлено: ${personState.persons.value.updated}` }}
        <a
          class="btn btn-link fs-5"
          href="#"
          style="text-decoration: none"
          :title="`Обновить`"
          @click="personState.getCandidates()"
        >
          <i class="bi bi-arrow-clockwise"/>
        </a>
      </caption>
      <thead>
        <tr height="50px">
          <th width="5%">#</th>
          <th width="15%">Регион</th>
          <th>Фамилия Имя Отчество</th>
          <th width="15%">Дата рождения</th>
          <th width="15%">Обновлено</th>
          <th width="15%">Сотрудник</th>
          <th width="5%" class="text-center">Статус</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="candidate in personState.persons.value.candidates"
          :key="candidate.id"
          height="50px"
          @click="openProfile(candidate.id)"
        >
          <td>{{ candidate.id }}</td>
          <td>{{ candidate.region }}</td>
          <td>
            {{
              `${candidate.surname} ${candidate.firstname} ${
                candidate.patronymic ? candidate.patronymic : ""
              }`
            }}
          </td>
          <td>
            {{ new Date(candidate.birthday).toLocaleDateString("ru-RU") }}
          </td>
          <td>
            {{ new Date(candidate.created).toLocaleDateString("ru-RU") }}
          </td>
          <td>
            {{
              candidate.username
                ? candidate.username.toString().split(" ")[0]
                : ""
            }}
          </td>
          <td class="text-center">
            <UIcon
              v-if="candidate.standing"
              name="i-heroicons-status-online"
            />
            <UIcon v-else name="i-heroicons-status-offline" />
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="p-3">Ничего не найдено</p>
    <nav
      v-if="personState.persons.value.prev || personState.persons.value.next"
      class="mb-4"
    >
      <UButtonGroup size="sm" orientation="horizontal">
        <UButton
          :disabled="!personState.persons.value.prev"
          variant="link"
          icon="i-heroicons-chevron-left"
          @click="
            personState.getCandidates(personState.persons.value.page - 1)
          "
        />
        <UButton
          :disabled="!personState.persons.value.next"
          variant="link"
          icon="i-heroicons-chevron-right"
          @click="
            personState.getCandidates(personState.persons.value.page + 1)
          "
        />
      </UButtonGroup>
    </nav>
  </LayoutsMenu>
</template>
