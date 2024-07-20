<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { debounce } from "@/utilities";
import { axiosAuth } from "@/auth";
import { server, stateAlert } from "@/state";
import { Persons } from "@/interfaces";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);

onBeforeMount(async () => {
  stateAlert.alertMessage.show = false;
  await getCandidates();
});

const personData = ref({
  candidates: <Persons[]>[],
  page: 1,
  prev: false,
  next: false,
  search: "",
  updated: `${new Date().toLocaleDateString(
    "ru-RU"
  )} в ${new Date().toLocaleTimeString("ru-RU")}`,
});

async function getCandidates(page = 1): Promise<void> {
  personData.value.page = page;
  try {
    const response = await axiosAuth.get(
      `${server}/index/${personData.value.page}`,
      {
        params: {
          search: personData.value.search,
        },
      }
    );
    [
      personData.value.candidates,
      personData.value.next,
      personData.value.prev,
    ] = response.data;

    personData.value.updated = `${new Date().toLocaleDateString(
      "ru-RU"
    )} в ${new Date().toLocaleTimeString("ru-RU")}`;
  } catch (error: any) {
    console.error(error);
  }
}

const searchPerson = debounce(() => {
  getCandidates();
}, 500);

function openProfile (person_id: string) {
  router.push({ name: "profile", params: { id: person_id } });
}
</script>

<template>
  <HeaderDiv :page-header="'Кандидаты'" />
  
  <div class="row mb-3">
    <form class="form form-check" role="form">
      <input
        @input.prevent="searchPerson"
        class="form-control"
        name="search"
        id="search"
        type="text"
        placeholder="поиск по фамилии, имени, отчеству, инн"
        v-model="personData.search"
      />
    </form>
  </div>
  <TableSlots 
    :class="'table align-middle table-hover'"
    v-if="personData.candidates.length"
    >
    <template v-slot:caption>{{ `Обновлено: ${personData.updated}` }}
      <a 
        class="btn btn-link fs-5" 
        href="#" 
        style="text-decoration: none;"
        :title="`Обновить`" 
        @click="getCandidates()"
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
        v-for="candidate in personData.candidates"
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
            class="spinner-grow spinner-grow-sm text-danger"
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
  <nav v-if="personData.prev || personData.next">
    <ul class="pagination justify-content-center py-3">
      <li class="page-item" :class="{disabled: !personData.prev}">
        <a
          class="page-link"
          href="#"
          @click="getCandidates(personData.page - 1)"
        >
          Предыдущая
        </a>
      </li>
      <li class="page-item" :class="{disabled: !personData.next}">
        <a
          class="page-link"
          href="#"
          @click="getCandidates(personData.page + 1)"
        >
          Следующая
        </a>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
tbody td {
  cursor: pointer;
}
</style>