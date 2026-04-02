<script setup lang="ts">
import type { FetchResponse } from "ofetch";
import type { TableColumn } from "@nuxt/ui";
import type { Candidate, Person, PersonId } from "@/types";

const toast = useToast();
const { $api } = useNuxtApp();
const candidates = useCandidateStore();
const person = usePersonStore();
const session = useSessionStore();

// Объявляем переменные для работы с данными
const modal = ref(false); // Состояние модального окна
const page = ref(1); // Страница таблицы
const per_page = 10; // Количество строк в таблице
const search = ref("");

// Определяем функцию для получения списка кандидатов из API
const { status, refresh } = await useLazyAsyncData(
  "candidates",
  () => candidates.getData(per_page, search.value),
  {
    watch: [page],
    default: () => [] as Candidate[],
  },
);

// Наблюдаем: поиск
watch(refDebounced(search, 1000), () => {
  if (page.value === 1) refresh();
  else page.value = 1;
});

// Определяем обработчики диалогового окна для загрузки JSON
const { open, onChange } = useFileDialog({
  accept: ".json",
  multiple: false,
});

// Фукция загрузки файла JSON
onChange(async (files) => {
  status.value = "pending";
  const str = (await files?.[0]?.text()) as string;
  try {
    const response = await $api.raw<Partial<PersonId>>("/routes/json", {
      method: "POST",
      body: JSON.parse(str),
    });
    proceedSubmit(response);
  } catch (error) {
    console.error(error);
  }
});

async function personSubmit(form: Person) {
  modal.value = false;
  const response = await person.addPerson(form);
  proceedSubmit(response);
}

// Обработчик результата загрузки данных
async function proceedSubmit(response: FetchResponse<Partial<PersonId>>) {
  if (response.status === 201) {
    toast.add({
      icon: "i-lucide-triangle-alert",
      title: "Успех",
      description:
        "Анкета загружена. Проверьте корректность данных, если анкета была содана ранее",
      color: "success",
    });
    const data = await response.json();
    return navigateTo("/profile/" + data.person_id);
  } else {
    status.value = "error";
    toast.add({
      icon: "i-lucide-triangle-alert",
      title: "Ошибка",
      description: "Ошибка данных или анкета существуетю",
      color: "error",
    });
  }
}

// Определяем массив данных для таблицы кандидатов
const columns: TableColumn<Candidate>[] = [
  { accessorKey: "id", header: "#" },
  {
    accessorKey: "surname",
    header: "Фамилия",
  },
  {
    accessorKey: "firstname",
    header: "Имя",
  },
  {
    accessorKey: "patronymic",
    header: "Отчество",
    cell: ({ row }) => {
      return row.getValue("patronymic") ?? "";
    },
  },
  {
    accessorKey: "birthday",
    header: "Дата рождения",
    cell: ({ row }) => {
      return new Date(row.getValue("birthday")).toLocaleDateString();
    },
  },
  {
    accessorKey: "editable",
    header: "Статус",
    cell: ({ row }) => {
      return h(resolveComponent("UIcon"), {
        name: !row.getValue("editable")
          ? "i-lucide-circle-check"
          : "i-lucide-triangle-alert",

        class: !row.getValue("editable")
          ? "text-start w-5 h-5 text-blue-600"
          : "text-start w-5 h-5 text-red-600",
        title: !row.getValue("editable")
          ? "Анкета доступна для редактирования"
          : "Анкета в режиме редактирования",
      });
    },
  },
  {
    accessorKey: "updated_at",
    header: "Обновлено",
    cell: ({ row }) => {
      return h(resolveComponent("NuxtTime"), {
        datetime: new Date(row.getValue("updated_at")).getTime() - 60000,
        relative: true,
      });
    },
  },
  {
    accessorKey: "username",
    header: "Сотрудник",
    cell: ({ row }) => {
      return row.original.username.split(" ")[0];
    },
  },
];
</script>

<template>
  <UContainer>
    <UPageHeader title="КАНДИДАТЫ" :ui="{ title: 'text-red-800' }">
      <template #links>
        <!-- меню для действий -->
        <UDropdownMenu
          v-if="session.user?.role === 'user'"
          :items="[
            {
              label: 'Создать анкету',
              icon: 'i-lucide-user-plus',
              onSelect() {
                modal = true;
              },
            },
            {
              label: 'Загрузить json',
              icon: 'i-lucide-upload',
              onSelect() {
                open();
              },
            },
          ]"
          :content="{ align: 'end' }"
        >
          <UButton
            icon="i-lucide-menu"
            variant="ghost"
            title="Действия"
            :loading="status === 'pending'"
          />
        </UDropdownMenu>
        <!-- Модальное окно для добавления анкеты -->
        <UModal
          v-model:open="modal"
          title="Анкета"
          description="Введите анкетные данные кандидата"
        >
          <template #body>
            <FormsResumeForm
              @update="personSubmit"
              @pending="status === 'pending'"
            />
          </template>
        </UModal>
      </template>
    </UPageHeader>

    <!-- Строка поиска -->
    <div class="my-6">
      <UInput
        id="search"
        v-model="search"
        type="search"
        icon="i-lucide-search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />
    </div>

    <!-- Таблица с данными кандидатов -->
    <UTable
      loading-animation="swing"
      empty="Данные не найдены"
      :loading="status === 'pending'"
      :columns="columns"
      :data="candidates.data"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="(_, row) => navigateTo(`/profile/${row.original.id}`)"
    >
      <template #loading>
        <UIcon name="i-lucide-refresh-ccw" mode="css" class="animate-spin" />
      </template>
    </UTable>

    <!-- Кнопка обновления и показа времени обновления -->
    <div class="my-2">
      <UButton
        variant="ghost"
        icon="i-lucide-refresh-ccw"
        title="Обновить данные"
        :loading="status === 'pending'"
        @click="refresh()"
      >
        Обновлено:
        <NuxtTime :datetime="candidates.updated" relative />
      </UButton>
    </div>

    <!-- Пагинация -->
    <div class="flex justify-center border-t border-default space-x-2 py-4">
      <UPagination
        v-model:page="page"
        :items-per-page="per_page"
        :total="candidates.total"
        :sibling-count="-1"
        @update:page="(p) => (page = p)"
      />
    </div>
  </UContainer>
</template>
