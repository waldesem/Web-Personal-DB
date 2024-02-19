<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount } from "vue";
import { profileStore } from "@/store/profile";
import { classifyStore } from "@/store/classify";

const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);

const storeProfile = profileStore();
const storeClassify = classifyStore();

onBeforeMount(() => {
  storeProfile.dataResume.getResume();
});
</script>

<template>
  <RowDivSlot :slotTwo="true">
    <template v-slot:divTwo>
      <a
        href="#"
        title="Изменить"
        @click="
          storeProfile.dataProfile.openForm(
            'resume',
            'update',
            storeProfile.dataResume.resume['id'],
            storeProfile.dataResume.resume
          )
        "
      >
        <i class="bi bi-pencil-square"></i>
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot
    :label="'Категория'"
    :value="
      storeClassify.classData.category[
        storeProfile.dataResume.resume['category_id']
      ]
    "
  />
  <RowDivSlot 
    :label="'Регион'"
    :value="storeClassify.classData.regions[
      storeProfile.dataResume.resume['region_id']
      ]"
  />
  <RowDivSlot
    :label="'Фамилия Имя Отчество'"
    :value="storeProfile.dataResume.resume['fullname']"
  />
  <RowDivSlot
    :label="'Изменение имени'"
    :value="storeProfile.dataResume.resume['previous']"
  />
  <RowDivSlot
    :label="'Дата рождения'"
    :value="storeProfile.dataResume.resume['birthday']"
  />
  <RowDivSlot
    :label="'Место рождения'"
    :value="storeProfile.dataResume.resume['birthplace']"
  />
  <RowDivSlot
    :label="'Гражданство'"
    :value="storeProfile.dataResume.resume['country']"
  />
  <RowDivSlot
    :label="'Второе гражданство'"
    :value="storeProfile.dataResume.resume['ext_country']"
  />
  <RowDivSlot
    :label="'СНИЛС'"
    :value="storeProfile.dataResume.resume['snils']"
  />
  <RowDivSlot :label="'ИНН'" :value="storeProfile.dataResume.resume['inn']" />
  <RowDivSlot
    :label="'Образование'"
    :value="storeProfile.dataResume.resume['education']"
  />
  <RowDivSlot
    :label="'Дополнительная информация'"
    :value="storeProfile.dataResume.resume['addition']"
  />
  <RowDivSlot :label="'Материалы'" :slotTwo="true" :print="true">
    <template v-slot:divTwo>
      <router-link
        :to="{
          name: 'manager',
          params: { group: 'staffsec' },
          query: { path: storeProfile.dataResume.resume['path'].split('/') },
        }"
      >
        {{ storeProfile.dataResume.resume["path"] }}
      </router-link>
    </template>
  </RowDivSlot>
  <RowDivSlot :label="'Статус'" :slotTwo="true">
    <template v-slot:divTwo>
      <a
        href="#"
        @click="storeProfile.dataResume.getResume('status')"
      >
        {{
          storeClassify.classData.status[
            storeProfile.dataResume.resume["status_id"]
          ]
        }}
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot
    :label="'Создан'"
    :value="
      new Date(
        String(storeProfile.dataResume.resume['created'])
      ).toLocaleDateString('ru-RU')
    "
  />
  <RowDivSlot
    :label="'Обновлен'"
    :value="
      new Date(
        String(storeProfile.dataResume.resume['updated'])
      ).toLocaleDateString('ru-RU')
    "
  />
  <RowDivSlot
    :label="'Внешний ID'"
    :value="storeProfile.dataResume.resume['request_id']"
  />
</template>
