<script setup lang="ts">
import { onBeforeMount } from "vue";
import { debounce } from "@/utils/utilities";
import * as state from "@/utils/state";

onBeforeMount(async () => {
  state.stateAlert.alertMessage.show = false;
  await state.statePersons.getCandidates();
});

const userState = stateUser();
const classifyState = stateClassify();

const searchPerson = debounce(() => {
  state.statePersons.getCandidates();
}, 500);

function openProfile (person_id: string) {
  const router = useRouter();
  router.push(`/profile/${person_id}`);
}
</script>

<template>
  <LayoutsMenu>
  <ElementsHeaderDiv :page-header="'Кандидаты'" />
  <div 
    v-if="userState.user.value.role == classifyState.classes.value.roles['user']" 
    class="position-relative"
  >
    <div class="position-absolute bottom-100 end-0 px-3">
      <label
        title="Загрузить json"
        for="file" 
        class="text-primary fs-5"
        style="cursor: pointer;"
      >Загрузить
        <i class="bi bi-filetype-json fs-5"></i>
      </label>
      <FormsFileForm :accept="'.json'" @submit="state.stateAnketa.submitFile($event, 'persons', '0')" />
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
        v-model="state.statePersons.persons.search"
      />
    </form>
  </div>
  <ElementsTableSlots 
    :tbl-class="'table align-middle table-hover'"
    v-if="state.statePersons.persons.candidates.length"
    >
    <template v-slot:caption>{{ `Обновлено: ${state.statePersons.persons.updated}` }}
      <a 
        class="btn btn-link fs-5" 
        href="#" 
        style="text-decoration: none;"
        :title="`Обновить`" 
        @click="state.statePersons.getCandidates()"
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
        v-for="candidate in state.statePersons.persons.candidates"
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
          {{ new Date (candidate.created).toLocaleDateString("ru-RU") }}
        </td>
        <td>
          {{
            candidate.username ? candidate.username.toString().split(" ")[0] : ""
          }}
        </td>
        <td class="text-center">
          <div
            v-if="candidate.standing"
            class="spinner-border spinner-grow-sm text-danger"
            role="status"
            :title="'Проверка'"
          >
          </div>
          <div v-else class="text-success fs-5" title="Окончено"><i class="bi bi-emoji-smile"></i>
          </div>
        </td>
      </tr>
    </template>
  </ElementsTableSlots>
  <p class="fs-6 taxt-danger" v-else>Ничего не найдено</p>
  <nav
    v-if="state.statePersons.persons.prev || state.statePersons.persons.next"
    class="mb-4">
    <ul class="pagination justify-content-center">
      <li class="page-item">
        <button
          :disabled="!state.statePersons.persons.prev"
          type="button"
          class="btn btn-link btn-outline-primary" 
          @click="state.statePersons.getCandidates(state.statePersons.persons.page - 1)"
        >
          <i class="bi bi-chevron-double-left"></i>
          Назад 
      </button>
      </li>
      <li class="page-item">
        <button 
          :disabled="!state.statePersons.persons.next"
          type="button" 
          class="btn btn-link btn-outline-primary" 
          @click="state.statePersons.getCandidates(state.statePersons.persons.page + 1)"
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