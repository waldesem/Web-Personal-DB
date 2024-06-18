<script setup lang="ts">
import {  defineAsyncComponent, onBeforeMount, ref } from "vue";
import { debounce, server, timeSince } from "@/utilities";
import { stateAlert } from "@/state";
import { axiosAuth } from "@/auth";
import { Resume } from "@/interfaces";
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
  "Проверка": "primary",
  "ПФО": "info",
  "Окончено": "secondary",
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
  candidates: <Resume[]>[],
  page: 1,
  prev: false,
  next: false,
  search: "",
  sort: "id",
  order: "desc",
  spinner: false,
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
          sort: personData.value.sort,
          order: personData.value.order,
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
    if (error.request.status == 401 || error.request.status == 403) {
      router.push({ name: "login" });
    } else {
      console.error(error);
    }
  }
}

function sortCandidates(sort: string, order: string): void {
  personData.value.sort = sort;
  personData.value.order = order;
  getCandidates();
}

const searchPerson = debounce(() => {
  getCandidates();
}, 500);

const formData = ref(new FormData());

async function submitFile(event: Event): Promise<void> {
  personData.value.spinner = true;
  const inputElement = event.target as HTMLInputElement;
  if (inputElement.files) {
    formData.value.append("file", inputElement.files[0]);
    try {
      const response = await axiosAuth.post(
        `${server}/file/anketa/0`,
        formData.value
      );
      console.log(response.status);
      getCandidates();

      stateAlert.setAlert("alert-success", "Файл успешно загружен");
    } catch (error) {
      console.error(error);
    }
  } else {
    stateAlert.setAlert("alert-warning", "Ошибка при загрузке файла");
  }
  personData.value.spinner = false;
}

const shortName = (fullname: string) => {
  const [first, second] = fullname.split(" ", )
  return `${first} ${second}}`
}
</script>

<template>
  <HeaderDiv :page-header="'Кандидаты'" />
  <div class="position-relative">
    <div class="position-absolute bottom-100 end-0">
      <span v-if="personData.spinner" class="spinner-border"></span>
      <label for="file" class="text-primary">
        <i
          class="bi bi-cloud-arrow-down fs-1"
          title="Загрузить анкету"
          style="cursor: pointer"
        >
        </i>
      </label>
      <FileForm :accept="'.json'" @submit="submitFile" />
    </div>
  </div>
  <div class="row mb-3">
    <form 
      class="form form-check" 
      role="form"
    >
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
    v-if="personData.candidates.length"
    :div-class="'table align-middle py-3'"
  >
    <template v-slot:caption>
      {{ `Обновлено: ${personData.updated}` }}
      <a href="#" :title="`Обновить`" @click="getCandidates()">
        <i class="bi bi-arrow-clockwise"></i>
      </a>
    </template>
    <template v-slot:thead>
      <tr height="50px">
        <th v-for="(thead, key) in theadData" :key="key" :width="thead[1]">
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
            :class="`fs-6 badge bg-${statusColor[candidate.status as keyof typeof statusColor]}`"
          >
            {{ candidate.status  }}
          </label>
        </td>
        <td>
          {{ timeSince(candidate.created) }}
        </td>
        <td>
          {{ candidate.username ? shortName(candidate.username.toString()) : "" }}
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
