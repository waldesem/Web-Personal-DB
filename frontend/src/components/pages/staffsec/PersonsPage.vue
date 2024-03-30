<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { classifyStore } from "@store/classify";
import { authStore } from "@/store/auth";
import { debounce, server, timeSince } from "@utilities/utils";
import { Resume } from "@/interfaces/interface";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const SelectInput = defineAsyncComponent(
  () => import("@components/content/elements/SelectInput.vue")
)
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);
const UpDown = defineAsyncComponent(
  () => import("@components/content/elements/UpDown.vue")
)
const PageSwitcher = defineAsyncComponent(
  () => import("@components/content/layouts/PageSwitcher.vue")
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
  },
  prev: false,
  next: false,
  search: "",
  sort: "id",
  order: "desc",
  page: 1,
  path: "main",
});

async function getCandidates (page = 1): Promise<void> {
  personData.value.page = page;
  try {
    const response = await storeAuth.axiosInstance.get(
      `${server}/index/${personData.value.path}/${personData.value.page}`,
      {
        params: {
          search: personData.value.search,
          sort: personData.value.sort,
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

function sortCandidates (sort: string, order: string): void {
  personData.value.sort = sort;
  personData.value.order = order;
  getCandidates(1);
}

const searchPerson = debounce(() => {
  personData.value.path = "search"
  getCandidates();
}, 500);
</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="header" />
    <div class="row mb-5">
      <div class="col-md-3">
        <form  class="form form-check" role="form"> 
          <SelectInput
            :name="'action'"
            :select="personData.items"
            v-model="personData.path"
            @submit-data="getCandidates"
          />
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
            name="search"
            id="search"
            type="text"
            placeholder="поиск по ФИО, ИНН"
            v-model="personData.search"
          />
        </form>
      </div>
    </div>
    <TableSlots 
      v-if="personData.candidates.length"
      :tbl-caption="'Список кандидатов'"
    >
      <template v-slot:thead>
        <tr height="50px">
          <th width="5%">
            #
            <UpDown
              :order="'desc'"
              :sort="'id'"
              @get-candidates="sortCandidates"
            />
            <UpDown
              :order="'asc'"
              :sort="'id'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th width="20%">
            Регион
            <UpDown
              :order="'desc'"
              :sort="'region_id'"
              @get-candidates="sortCandidates"
            />
            <UpDown
              :order="'asc'"
              :sort="'region_id'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th>
            Фамилия Имя Отчество
            <UpDown
              :order="'desc'"
              :sort="'surname'"
              @get-candidates="sortCandidates"
            />
            <UpDown
              :order="'asc'"
              :sort="'surname'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th width="15%">
            Дата рождения
            <UpDown
              :order="'desc'"
              :sort="'birthday'"
              @get-candidates="sortCandidates"
            />
            <UpDown
              :order="'asc'"
              :sort="'birthday'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th width="10%">
            Статус
            <UpDown
              :order="'desc'"
              :sort="'status_id'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th width="15%">
            Создан
            <UpDown
              :order="'desc'"
              :sort="'created'"
              @get-candidates="sortCandidates"
            />
            <UpDown
              :order="'asc'"
              :sort="'created'"
              @get-candidates="sortCandidates"
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
          <td>{{ candidate["id"] }}</td>
          <td>{{ storeClassify.classData.regions[candidate.region_id] }}</td>
          <td>
            <router-link
              :to="{
                name: 'profile',
                params: { id: candidate.id },
              }"
            >
              {{ `${candidate.surname} ${candidate.firstname} ${candidate.patronymic ? candidate.patronymic : ''}` }}
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
      </template>
    </TableSlots>
    <PageSwitcher
      :has_prev="personData.prev"
      :has_next="personData.next"
      :switchPrev="personData.page - 1"
      :switchNext="personData.page + 1"
      @switch="getCandidates"
    />
  </div>
</template>
