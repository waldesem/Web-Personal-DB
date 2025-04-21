<script setup lang="ts">
import type { Persons, Relation } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {} as Relation,
  },
});

const authFetch = useFetchAuth();

const relationForm = ref(props.relation as Relation);

/* Get persons list for searchable select */
async function search(query: string) {
  if (query.length < 2) return [];
  const { results } = (await authFetch("/route/index/1", {
    params: {
      search: query,
      editable: false,
    },
  })) as Record<string, unknown> as { results: Persons[] };

  const persons = [] as { id: string; name: string }[];
  results.forEach((result: Persons) => {
    persons.push({
      id: result.id,
      name:
        result.surname +
        " " +
        result.firstname +
        " " +
        result.patronymic +
        " - " +
        new Date(result.birthday).toLocaleDateString("ru-RU"),
    });
  });
  return persons;
}
</script>

<template>
  <UForm :state="relationForm" @submit.prevent="emit('update', relationForm)">
    <UFormField class="mb-3" label="Тип связи" name="type" required>
      <USelect
        v-model="relationForm.type"
        required
        :items="[
          'Одно лицо',
          'Родители-Дети',
          'Братья-Сестры',
          'Супруг-Супруга',
          'Родственники',
          'Родственники',
        ]"
        placeholder="Тип связи"
      />
    </UFormField>
    <UFormField class="mb-3" label="ID связи" name="right_id" required>
      <USelectMenu
        v-model="relationForm.right_id"
        :searchable="search"
        :debounce="1000"
        :searchable-lazy="true"
        option-attribute="name"
        value-attribute="id"
        searchable-placeholder="Поиск по ФИО"
        clear-search-on-close
        required
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
