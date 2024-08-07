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
  const router = useRouter();
  navigateTo(`/profile/${person_id}`);
}
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv :page-header="'Кандидаты'" />
    <div
      v-if="
        userState.user.value.role == classifyState.classes.value.roles['user']
      "
      class="position-relative"
    >
      <div class="position-absolute bottom-100 end-0 px-3">
        <label
          title="Загрузить json"
          for="file"
          class="text-primary fs-5"
          style="cursor: pointer"
          >Загрузить
          <i class="bi bi-filetype-json fs-5"></i>
        </label>
        <FormsFileForm
          :accept="'.json'"
          @submit="anketaState.submitFile($event, 'persons', '0')"
        />
      </div>
    </div>
    <div class="row mb-3">
      <form class="form form-check" role="form">
        <input
          @input.prevent="searchPerson"
          class="form-control"
          name="search"
          id="search"
          type="text"
          placeholder="поиск по фамилии, имени, отчеству, дате рождения, инн"
          v-model="personState.persons.value.search"
        />
      </form>
    </div>
    <ElementsTableSlots
      :tbl-class="'table align-middle table-hover'"
      v-if="personState.persons.value.candidates.length"
    >
      <template v-slot:caption
        >{{ `Обновлено: ${personState.persons.value.updated}` }}
        <a
          class="btn btn-link fs-5"
          href="#"
          style="text-decoration: none"
          :title="`Обновить`"
          @click="personState.getCandidates()"
        >
          <i class="bi bi-arrow-clockwise"></i>
        </a>
      </template>
      <template v-slot:thead>
        <tr height="50px">
          <th width="5%">#</th>
          <th width="15%">Регион</th>
          <th>Фамилия Имя Отчество</th>
          <th width="15%">Дата рождения</th>
          <th width="15%">Обновлено</th>
          <th width="15%">Сотрудник</th>
          <th width="5%" class="text-center">Статус</th>
        </tr>
      </template>
      <template v-slot:tbody>
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
            <div
              v-if="candidate.standing"
              class="spinner-border spinner-grow-sm text-danger"
              role="status"
              :title="'Проверка'"
            ></div>
            <div v-else class="text-success fs-5" title="Окончено">
              <i class="bi bi-emoji-smile"></i>
            </div>
          </td>
        </tr>
      </template>
    </ElementsTableSlots>
    <p class="fs-6 taxt-danger" v-else>Ничего не найдено</p>
    <nav
      v-if="personState.persons.value.prev || personState.persons.value.next"
      class="mb-4"
    >
      <ul class="pagination justify-content-center">
        <li class="page-item">
          <button
            :disabled="!personState.persons.value.prev"
            type="button"
            class="btn btn-link btn-outline-primary"
            @click="
              personState.getCandidates(personState.persons.value.page - 1)
            "
          >
            <i class="bi bi-chevron-double-left"></i>
            Назад
          </button>
        </li>
        <li class="page-item">
          <button
            :disabled="!personState.persons.value.next"
            type="button"
            class="btn btn-link btn-outline-primary"
            @click="
              personState.getCandidates(personState.persons.value.page + 1)
            "
          >
            Вперёд
            <i class="bi bi-chevron-double-right"></i>
          </button>
        </li>
      </ul>
    </nav>
  </LayoutsMenu>
</template>

<style scoped>
td {
  cursor: pointer;
}
</style>
