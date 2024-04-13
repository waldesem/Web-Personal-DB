<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { classifyStore } from "@store/classify";
import { authStore } from "@/store/auth";
import { debounce, server, timeSince } from "@utilities/utils";
import { Resume } from "@/interfaces/interface";

const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);
const IconRelative = defineAsyncComponent(
  () => import("@components/content/elements/IconRelative.vue")
);
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

const storeAuth = authStore();
const storeClassify = classifyStore();

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
    "9": "light",
    "10": "warning",
    "11": "light",
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
  updated: new Date().toLocaleDateString("ru-RU"),
});

async function getCandidates(page = 1): Promise<void> {
  personData.value.page = page;
  try {
    const response = await storeAuth.axiosInstance.get(
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
    personData.value.updated = new Date().toLocaleDateString("ru-RU");
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
  getCandidates();
}, 500);
</script>

<template>
  <!-- <div class="container py-3"> -->
    <AlertMessage/>
    <div class="row mb-5">
      <HeaderDiv :page-header="'Кандидаты'" />
      <IconRelative
        :title="`Обновить`"
        :icon-class="`bi bi-arrow-clockwise fs-1`"
        @onclick="getCandidates"
      />
    </div>
    <div class="row mb-5">
      <div class="col-md-3">
        <SelectObject
          :name="'action'"
          :select="personData.items"
          v-model="personData.path"
          @submit-data="getCandidates"
        />
      </div>
      <div class="col-md-9">
        <input
          @input.prevent="searchPerson"
          class="form-control"
          name="search"
          id="search"
          type="text"
          placeholder="поиск по ФИО, ИНН"
          v-model="personData.search"
        />
      </div>
    </div>
    <TableSlots
      v-if="personData.candidates.length"
      :div-class="'table align-middle caption-top'"
      :tbl-caption="`Обновлено: ${timeSince(personData.updated)}`"
    >
      <template v-slot:thead>
        <tr height="50px">
          <th width="10%">
            #
            <AscDesc
              :order="'desc'"
              :sort="'id'"
              @get-candidates="sortCandidates"
            />
            <AscDesc
              :order="'asc'"
              :sort="'id'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th width="20%">
            Регион
            <AscDesc
              :order="'desc'"
              :sort="'region_id'"
              @get-candidates="sortCandidates"
            />
            <AscDesc
              :order="'asc'"
              :sort="'region_id'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th>
            Фамилия Имя Отчество
            <AscDesc
              :order="'desc'"
              :sort="'surname'"
              @get-candidates="sortCandidates"
            />
            <AscDesc
              :order="'asc'"
              :sort="'surname'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th width="15%">
            Дата рождения
            <AscDesc
              :order="'desc'"
              :sort="'birthday'"
              @get-candidates="sortCandidates"
            />
            <AscDesc
              :order="'asc'"
              :sort="'birthday'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th width="15%">
            Статус
            <AscDesc
              :order="'desc'"
              :sort="'status_id'"
              @get-candidates="sortCandidates"
            />
            <AscDesc
              :order="'asc'"
              :sort="'status_id'"
              @get-candidates="sortCandidates"
            />
          </th>
          <th width="15%">
            Создан
            <AscDesc
              :order="'desc'"
              :sort="'created'"
              @get-candidates="sortCandidates"
            />
            <AscDesc
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
            {{ storeClassify.classData.status[candidate.status_id] }}
            </label>
          </td>
          <td>
            {{ timeSince(candidate.created) }}
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
  <!-- </div> -->
</template>
