<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { debounce } from "@/utilities";
import { axiosAuth } from "@/auth";
import { stateClassify, server } from "@/state";
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
    case "Правка":
      return "danger";
    case "ПФО":
      return "info";
    case "Окончено":
      return "secondary";
    case "Сохранено":
      return "warning";
  }
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
    console.error(error);
  }
}

const searchPerson = debounce(() => {
  getCandidates();
}, 500);
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
        <th width="5%">#</th>
        <th width="13%">Регион</th>
        <th>Фамилия Имя Отчество</th>
        <th width="13%">Дата рождения</th>
        <th width="13%">Статус</th>
        <th width="13%">Обновлено</th>
        <th width="13%">Сотрудник</th>
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
            :class="`fs-6 badge bg-${statusColor(candidate.standing)}`"
          >
            {{ candidate.standing }}
          <span
            v-if="candidate.standing == stateClassify.standing['manual']"
            class="spinner-grow spinner-grow-sm"
            role="status"
          >
          </span>
        </label>

        </td>
        <td>
          {{ new Date (candidate.created).toLocaleDateString("ru-RU") }}
        </td>
        <td>
          {{
            candidate.username ? candidate.username.toString().split(" ")[0] : ""
          }}
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
