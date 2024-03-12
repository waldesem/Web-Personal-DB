<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { classifyStore } from "@store/classify";
import { authStore } from "@/store/auth";
import { debounce, server, timeSince } from "@utilities/utils";
import { Resume } from "@/interfaces/interface";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const PageSwitcher = defineAsyncComponent(
  () => import("@components/layouts/PageSwitcher.vue")
);

const storeAuth = authStore();
const storeClassify = classifyStore();

const header = computed(() => {
  return personData.value.items[
    personData.value.path as keyof typeof personData.value.items
  ];
});

onBeforeMount( async () => {
  await getCandidates();
});

const personData = ref({
  candidates: <Resume[]>[],
  items: {
    search: "Результаты поиска",
    officer: "Страница пользователя",
    main: "Все кандидаты",
    new: "Новые кандидаты",
  },
  prev: false,
  next: false,
  search: "",
  page: 1,
  path: "new",
});

async function getCandidates (page = 1): Promise<void> {
  personData.value.page = page;
  try {
    const response = await storeAuth.axiosInstance.get(
      `${server}/index/${personData.value.path}/${personData.value.page}`,
      {
        params: {
          search: personData.value.search,
        },
      }
    );
    const [datas, metadata] = response.data;
    personData.value.candidates = datas;
    personData.value.prev = metadata.has_prev;
    personData.value.next = metadata.has_next;
  } catch (error) {
    console.error(error);
  }
};

const searchPerson = debounce(() => {
  personData.value.path = "search"
  getCandidates();
}, 500);

function changePath (): void {
  getCandidates();
};
</script>

<template>
      <div class="container py-3">
    <HeaderDiv :page-header="header" />
    <div class="row">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <label class="visually-hidden" for="action"></label>
          <select
            class="form-select"
            required
            id="action"
            name="action"
            v-model="personData.path"
            @change="changePath"
          >
            <option
              v-for="(value, key) in personData.items"
              :key="key"
              :value="key"
              :selected="key === 'new'"
            >
              {{ value }}
            </option>
          </select>
        </form>
      </div>
      <div class="col-md-9">
        <form 
          @input.prevent="searchPerson" 
          class="form form-check" 
          role="form"
        >
          <input
            class="form-control"
            id="data"
            name="data"
            type="text"
            maxlength="250"
            minlength="3"
            placeholder="поиск по ФИО, ИНН"
            v-model="personData.search"
          />
        </form>
      </div>
    </div>
    <div class="py-3">
      <table class="table table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th width="20%">Регион</th>
            <th>Фамилия Имя Отчество</th>
            <th width="15%">Дата рождения</th>
            <th width="10%">Статус</th>
            <th width="15%"> Создан</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="candidate in personData.candidates"
            :key="candidate.id"
            height="50px"
          >
            <td>{{ candidate["id"] }}</td>
            <td>{{ storeClassify.classData.regions[candidate.region_id] }}</td>
            <td>
              <router-link
                :to="{
                  name: 'profile',
                  params: { id: candidate.id },
                }"
              >
                {{ `${candidate.surname} ${candidate.firstname} ${candidate.patronymic}` }}
              </router-link>
            </td>
            <td>
              {{ new Date(candidate.birthday).toLocaleDateString("ru-RU") }}
            </td>
            <td>{{ storeClassify.classData.status[candidate.status_id] }}</td>
            <td>
              {{ timeSince(candidate.created) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <PageSwitcher
      :has_prev="personData.prev"
      :has_next="personData.next"
      :switchPrev="personData.page - 1"
      :switchNext="personData.page + 1"
      @switch="getCandidates"
    />
  </div>
</template>
