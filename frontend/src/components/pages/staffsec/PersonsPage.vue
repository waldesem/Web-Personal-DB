<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount } from "vue";
import { debounce } from "@/utilities";
import { stateAlert, stateAnketa, statePersons } from "@/state";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);

const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);

onBeforeMount(async () => {
  stateAlert.alertMessage.show = false;
  await statePersons.getCandidates();
});

const searchPerson = debounce(() => {
  statePersons.getCandidates();
}, 500);

function openProfile (person_id: string) {
  router.push({ name: "profile", params: { id: person_id } });
}
</script>

<template>
  <HeaderDiv :page-header="'Кандидаты'" />
  <div class="position-relative">
    <div class="position-absolute bottom-100 end-0 px-3">
      <label
        for="file" 
        class="text-primary fs-5"
        style="cursor: pointer;"
      >Загрузить json
      &#9735;
      </label>
      <FileForm :accept="'.json'" @submit="stateAnketa.submitFile($event, 'persons', '0')" />
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
        v-model="statePersons.persons.search"
      />
    </form>
  </div>
  <TableSlots 
    :tbl-class="'table align-middle table-hover'"
    v-if="statePersons.persons.candidates.length"
    >
    <template v-slot:caption>{{ `Обновлено: ${statePersons.persons.updated}` }}
      <a 
        class="btn btn-link fs-5" 
        href="#" 
        style="text-decoration: none;"
        :title="`Обновить`" 
        @click="statePersons.getCandidates()"
      >
        &#8635
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
        v-for="candidate in statePersons.persons.candidates"
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
          <div v-else :title="'Окончено'">&#128994</div>
        </td>
      </tr>
    </template>
  </TableSlots>
  <p class="fs-6 taxt-danger" v-else>Ничего не найдено</p>
  <nav
    v-if="statePersons.persons.prev || statePersons.persons.next"
    class="mb-4">
    <ul class="pagination justify-content-center">
      <li class="page-item">
        <button
          :disabled="!statePersons.persons.prev"
          type="button"
          class="btn btn-link btn-outline-primary" 
          @click="statePersons.getCandidates(statePersons.persons.page - 1)"
        >
          <i class="bi bi-chevron-double-left"></i>
          Назад 
      </button>
      </li>
      <li class="page-item">
        <button 
          :disabled="!statePersons.persons.next"
          type="button" 
          class="btn btn-link btn-outline-primary" 
          @click="statePersons.getCandidates(statePersons.persons.page + 1)"
        >
          Вперёд
          <i class="bi bi-chevron-double-right"></i>
        </button>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
td {
  cursor: pointer;
}
</style>