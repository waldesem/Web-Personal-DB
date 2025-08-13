<script setup lang="ts">
import { useFileDialog, watchDebounced } from "@vueuse/core";
import type { DropdownMenuItem, TableColumn } from "@nuxt/ui";
import type { Candidate } from "@/types";

const { $api } = useNuxtApp();

await preloadRouteComponents("/profile/[id]");

const UIcon = resolveComponent("UIcon");
const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");
const NuxtTime = resolveComponent("NuxtTime");

const userState = useStateUser();

const page = ref(1);
const search = ref("");
const modal = ref(false);
const updated = ref(Date.now());
const per_page = 10;

const {
  data: candidates,
  status,
  refresh,
} = await useAPI<Candidate[]>("/route/index", {
  params: {
    search: search.value,
    per_page: per_page,
    page: page.value,
  },
  watch: [page],
  lazy: true,
  server: false,
});

watchDebounced(search, async () => await refresh(), {
  debounce: 1000,
  maxWait: 2000,
});

watch(candidates, () => (updated.value = Date.now()));

const { open, onChange } = useFileDialog({
  accept: ".json",
  multiple: false,
});

onChange(async (files) => {
  if (!files?.length) return;
  status.value = "pending";
  const formData = new FormData();
  formData.append("file", files[0] as File);
  const { person_id, exists } = await $api<{
    person_id: string;
    exists: boolean;
  }>("/route/json", {
    method: "POST",
    body: formData,
  });
  createToast(person_id, exists);
});

async function createToast(person_id: string, exists: boolean) {
  status.value = "success";
  if (person_id) {
    if (exists) {
      makeToast("info", "Кандидат ранее уже был загружен");
    } else {
      makeToast("success", "Анкета успешно загружена");
    }
    return navigateTo("/profile/" + person_id);
  } else {
    if (exists) {
      makeToast(
        "info",
        "Анкета находится в другом регионе или назначена иному пользователю"
      );
    } else {
      makeToast();
    }
  }
}

function submitResume(person_id: string, exists: boolean) {
  modal.value = false;
  createToast(person_id, exists);
}

const columns: TableColumn<Candidate>[] = [
  { accessorKey: "id", header: "#" },
  { accessorKey: "fullname", header: "Фамилия Имя Отчество" },
  {
    accessorKey: "birthday",
    header: "Дата рождения",
    cell: ({ row }) => {
      return h(NuxtTime, {
        datetime: row.original.birthday,
      });
    },
  },
  {
    accessorKey: "editable",
    header: "Статус",
    cell: ({ row }) => {
      return h(UIcon, {
        name: !row.original.editable
          ? "i-lucide-circle-check"
          : "i-lucide-triangle-alert",

        class: !row.original.editable
          ? "text-start w-5 h-5 text-blue-600"
          : "text-start w-5 h-5 text-red-600",
        title: !row.original.editable
          ? "Анкета доступна для редактирования"
          : "Анкета находится в режиме редактирования",
      });
    },
  },
  {
    accessorKey: "created",
    header: "Обновлено",
    cell: ({ row }) => {
      return h(NuxtTime, {
        datetime: row.original.created,
      });
    },
  },
  {
    accessorKey: "username",
    header: "Сотрудник",
    cell: ({ row }) => {
      try {
        return row.original.username.split(" ")[0];
      } catch {
        return "";
      }
    },
  },
];

const items: DropdownMenuItem[] = [
  {
    label: "Создать анкету",
    icon: "i-lucide-user-plus",
    onSelect() {
      modal.value = true;
    },
  },
  {
    label: "Загрузить json",
    icon: "i-lucide-upload",
    onSelect() {
      open();
    },
  },
];
</script>

<template>
  <div class="py-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-2xl text-red-800 font-bold">КАНДИДАТЫ</h3>
      <div v-if="userState.role == 'user'">
        <UDropdownMenu :items="items" :content="{ align: 'end' }">
          <UButton
            :loading="status === 'pending'"
            icon="i-lucide-ellipsis-vertical"
            variant="ghost"
            size="lg"
            title="Выбор действия"
          />
        </UDropdownMenu>

        <UModal
          v-model:open="modal"
          title="Добавить анкету"
          description="Введите анкетные данные кандидата"
        >
          <template #body>
            <LazyFormsResumeForm @update="submitResume" />
          </template>
        </UModal>
      </div>
    </div>

    <div class="my-6">
      <UInput
        id="search"
        v-model="search"
        type="search"
        icon="i-lucide-search"
        placeholder="поиск по фаимилии, имени, отчеству"
      />
    </div>

    <UTable
      :loading="status === 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
      :columns="columns"
      :data="candidates"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      @select="navigateTo(`/profile/${$event.original.id}`)"
    />

    <div class="my-2">
      <UButton
        variant="ghost"
        icon="i-lucide-refresh-ccw"
        :loading="status === 'pending'"
        title="Обновить данные"
        @click="refresh()"
        >Обновлено в
        <NuxtTime :datetime="updated" hour="2-digit" minute="2-digit" />
      </UButton>
    </div>

    <div class="flex justify-center border-t border-default py-4">
      <UPagination
        v-model:page="page"
        :items-per-page="per_page"
        :total="candidates?.[0]?.total ?? 1"
        :sibling-count="1"
        @update:page="(p) => (page = p)"
      />
    </div>
  </div>
</template>
