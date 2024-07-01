<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { debounce, timeSince } from "@/utilities";
import { authErrorHandler, axiosAuth } from "@/auth";
import { server } from "@/state";
import { Persons } from "@/interfaces";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);

onBeforeMount(async () => {
  await getCandidates();
});

const statusColor = (status: string) => {
  switch (status) {
    case "Проверка":
      return "primary";
    case "ПФО":
      return "info";
    case "Окончено":
      return "secondary";
    case "Сохранено":
      return "warning";
  }
};

const theadData = {
  id: ["#", "5%"],
  region_id: ["Регион", "15%"],
  surname: ["Фамилия Имя Отчество", "25%"],
  birthday: ["Дата рождения", "15%"],
  status: ["Статус", "10%"],
  created: ["Создан", "15%"],
  user: ["Сотрудник", "15%"],
};

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
    authErrorHandler(error);
  }
}

const searchPerson = debounce(() => {
  getCandidates();
}, 500);

const shortName = (fullname: string) => {
  const [first, second] = fullname.split(" ");
  return `${first} ${second}`;
};
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
  <TableSlots v-if="personData.candidates.length">
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
        <th v-for="(thead, key) in theadData" :key="key" :width="thead[1]">
          {{ thead[0] }}
        </th>
      </tr>
    </template>
    <template v-slot:tbody>
      <tr
        v-for="candidate in personData.candidates"
        :key="candidate.id"
        height="50px"
      >
        <td>{{ candidate.id }}</td>
        <td>{{ candidate.region }}</td>
        <td>
          <router-link
            :to="{
              name: 'profile',
              params: { id: candidate.id },
            }"
          >
            {{
              `${candidate.surname} ${candidate.firstname} ${
                candidate.patronymic ? candidate.patronymic : ""
              }`
            }}
          </router-link>
        </td>
        <td>
          {{ new Date(candidate.birthday).toLocaleDateString("ru-RU") }}
        </td>
        <td>
          <label
            :class="`fs-6 badge bg-${statusColor(candidate.status)}`"
          >
            {{ candidate.status }}
          </label>
        </td>
        <td>
          {{ timeSince(candidate.created) }}
        </td>
        <td>
          {{
            candidate.username ? shortName(candidate.username.toString()) : ""
          }}
        </td>
      </tr>
    </template>
  </TableSlots>
  <p v-else>Ничего не найдено</p>
  <nav v-if="personData.prev || personData.next">
    <ul class="pagination justify-content-center py-3">
      <li class="page-item" :disabled="!personData.prev">
        <a
          class="page-link"
          href="#"
          @click="getCandidates(personData.page - 1)"
        >
          Предыдущая
        </a>
      </li>
      <li class="page-item" :disabled="!personData.next">
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
