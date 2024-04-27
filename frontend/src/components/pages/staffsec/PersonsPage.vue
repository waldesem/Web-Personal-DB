<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { debounce, server, timeSince } from "@/utilities";
import { stateClassify } from "@/state";
import { axiosAuth } from "@/auth";
import { Resume } from "@/interfaces";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const SelectObject = defineAsyncComponent(
  () => import("@components/content/elements/SelectObject.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);
const AscDesc = defineAsyncComponent(
  () => import("@components/content/elements/AscDesc.vue")
);
const PageSwitcher = defineAsyncComponent(
  () => import("@components/content/elements/PageSwitcher.vue")
);

onBeforeMount(async () => {
  await getCandidates();
});

const statusColor = {
  "1": "success",
  "2": "success",
  "3": "success",
  "4": "primary",
  "5": "primary",
  "6": "danger",
  "7": "info",
  "8": "secondary",
  "9": "warning",
  "10": "secondary",
};

const theadData = {
  "id": ["#", "10%"],
  "region_id": ["Регион", "15%"],
  "surname": ["Фамилия Имя Отчество", "25%"],
  "birthday": ["Дата рождения", "15%"],
  "status_id": ["Статус", "10%"],
  "created": ["Создан", "10%"],
  "user_id": ["Сотрудник", "15%"],
}

const personData = ref({
  candidates: <Resume[]>[],
  items: {
    officer: "Мои кандидаты",
    search: "Все кандидаты",
  },
  page: 1,
  prev: false,
  next: false,
  search: "",
  sort: "id",
  order: "desc",
  path: "search",
  updated: `${new Date().toLocaleDateString(
    "ru-RU"
  )} в ${new Date().toLocaleTimeString("ru-RU")}`,
});

async function getCandidates(page = 1): Promise<void> {
  personData.value.page = page;
  try {
    const response = await axiosAuth.get(
      `${server}/index/${personData.value.path}/${personData.value.page}`,
      {
        params: {
          search: personData.value.search,
          sort: personData.value.sort,
          order: personData.value.order,
        },
      }
    );
    const [datas, metadata] = response.data;
    personData.value.candidates = datas;
    personData.value.prev = metadata.has_prev;
    personData.value.next = metadata.has_next;
    personData.value.updated = `${new Date().toLocaleDateString(
      "ru-RU"
    )} в ${new Date().toLocaleTimeString("ru-RU")}`;


  } catch (error) {
    console.error(error);
  }
}

function sortCandidates(sort: string, order: string): void {
  personData.value.sort = sort;
  personData.value.order = order;
  getCandidates();
}

const searchPerson = debounce(() => {
  personData.value.path = "search";
  if (personData.value.search.length < 3) {
    return;
  }
  getCandidates();
}, 500);
</script>

<template>
  <HeaderDiv :page-header="'Кандидаты'" />
  <div class="row mb-3">
    <div class="col-md-2">
      <SelectObject
        :name="'action'"
        :select="personData.items"
        v-model="personData.path"
        @submit-data="getCandidates"
      />
    </div>
    <div class="col-md-10">
      <input
        @input.prevent="searchPerson"
        class="form-control"
        name="search"
        id="search"
        type="text"
        placeholder="поиск по Фамилии, Имени, Отчеству, ИНН (не менее 3-х символов)"
        v-model="personData.search"
      />
    </div>
  </div>
  <TableSlots
    v-if="personData.candidates.length"
    :div-class="'table caption-top align-middle py-3'"
  >
    <template v-slot:caption>
      {{ `Обновлено: ${personData.updated}` }}
      <a href="#" :title="`Обновить`" @click="getCandidates()">
        <i class="bi bi-arrow-clockwise"></i>
      </a>
    </template>
    <template v-slot:thead>
      <tr height="50px">
        <th v-for="(thead, key) in theadData" :key="key" 
          :width="thead[1]">
          {{ thead[0] }}
          <AscDesc
            :order="'desc'"
            :sort="key"
            @sort-candidates="sortCandidates"
          />
          <AscDesc
            :order="'asc'"
            :sort="key"
            @sort-candidates="sortCandidates"
          />
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
        <td>{{ stateClassify.regions[candidate.region_id] }}</td>
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
            :class="`fs-6 badge bg-${statusColor[candidate.status_id as keyof typeof statusColor]}`"
          >
            {{ stateClassify.status[candidate.status_id] }}
          </label>
        </td>
        <td>
          {{ timeSince(candidate.created) }}
        </td>
        <td>
          {{
            candidate.user_id
              ? stateClassify.users[candidate.user_id].split(" ")[0]
              : ""
          }}
        </td>
      </tr>
    </template>
  </TableSlots>
  <p v-else>Ничего не найдено</p>
  <PageSwitcher
    :has_prev="personData.prev"
    :has_next="personData.next"
    :switchPrev="personData.page - 1"
    :switchNext="personData.page + 1"
    @switch="getCandidates"
  />
</template>
