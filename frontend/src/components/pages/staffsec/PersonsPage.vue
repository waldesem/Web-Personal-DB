<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { classifyStore } from "@store/classify";
import { authStore } from "@/store/auth";
import { debounce, server, timeSince } from "@utilities/utils";
import { Resume } from "@/interfaces/interface";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/elements/TableSlots.vue")
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
          <SelectDiv
            :lbl-class="'visually-hidden'"
            :label="'Таблица'"
            :slc-class="'col-md-12'"
            :name="'action'"
            :isneed="false"
            :select="personData.items"
            v-model="personData.path"
            @change-event="changePath"
          />
        </form>
      </div>
      <div class="col-md-9">
        <form 
          @input.prevent="searchPerson" 
          class="form form-check" 
          role="form"
        >
          <InputLabel
            :lbl-cls="'visually-hidden'"
            :cls-input="'col-lg-12'"
            :lbl="'Поиск'"
            :name="'search'"
            :placeholder="'поиск по ФИО, ИНН'"
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
          <th width="5%">#</th>
          <th width="20%">Регион</th>
          <th>Фамилия Имя Отчество</th>
          <th width="15%">Дата рождения</th>
          <th width="10%">Статус</th>
          <th width="15%"> Создан</th>
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
