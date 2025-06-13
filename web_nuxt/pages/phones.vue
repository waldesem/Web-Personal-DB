<script setup lang="ts">
import { watchDebounced } from "@vueuse/core";
import type { TableColumn } from "@nuxt/ui";
import type { Column } from "@tanstack/vue-table";
import type { Phone } from "@/types";

const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");

const search = ref("");
const items = ref([] as string[]);
const phones = shallowRef([] as Phone[]);
const phone = ref({} as Phone);
const modal = ref(false);
const expanded = ref({ 1: false });

const { refresh, status } = await useLazyAsyncData("users", async () => {
  const { results, organizations } = (await fetchAuth("/route/phones", {
    params: {
      search: search.value,
    },
  })) as Record<string, unknown> as {
    results: Phone[];
    organizations: string[];
  };
  phones.value = results;
  items.value = organizations;
});

watchDebounced(
  search,
  () => {
    refresh();
  },
  {
    debounce: 1000,
    maxWait: 2000,
  }
);

async function deletePhone(phone_id: string): Promise<void> {
  if (!confirm("Подтвердите выполнение действия")) return;
  const { message } = (await fetchAuth("/route/phones/" + phone_id, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    makeToast("success", "Действие успешно выполнено");
  } else {
    makeToast();
  }
  refresh();
}

function getRowItems(item: Phone) {
  return [
    {
      label: "Удалить",
      onSelect() {
        deletePhone(item.id);
      },
    },
    {
      label: "Изменить",
      onSelect() {
        phone.value = item;
        modal.value = true;
      },
    },
  ];
}

const columns: TableColumn<Phone>[] = [
  {
    id: "expand",
    cell: ({ row }) =>
      h(UButton, {
        color: "neutral",
        variant: "ghost",
        icon: "i-heroicons-chevron-down",
        square: true,
        ui: {
          leadingIcon: [
            "transition-transform",
            row.getIsExpanded() ? "duration-200 rotate-180" : "",
          ],
        },
        onClick: () => row.toggleExpanded(),
      }),
  },
  {
    accessorKey: "organization",
    header: ({ column }) => getHeader(column, "Организация"),
  },
  { accessorKey: "fullname", header: "Полное имя" },
  { accessorKey: "phone", header: "Телефон" },
  {
    accessorKey: "created",
    header: "Обновлено",
    cell: ({ row }) => {
      return new Date(row.original.created).toLocaleDateString("ru-RU");
    },
  },
  {
    id: "actions",
    cell: ({ row }) => {
      return h(
        "div",
        { class: "text-right" },
        h(
          UDropdownMenu,
          {
            content: {
              align: "end",
            },
            items: getRowItems(row.original),
            "aria-label": "Actions dropdown",
          },
          () =>
            h(UButton, {
              icon: "i-heroicons-ellipsis-vertical",
              color: "neutral",
              variant: "ghost",
              class: "ml-auto",
            })
        )
      );
    },
  },
];

function getHeader(column: Column<Phone>, label: string) {
  const isSorted = column.getIsSorted();

  return h(
    UDropdownMenu,
    {
      content: {
        align: "start",
      },
      "aria-label": "Actions dropdown",
      items: [
        {
          label: "Asc",
          type: "checkbox",
          icon: "i-lucide-arrow-up-narrow-wide",
          checked: isSorted === "asc",
          onSelect: () => {
            if (isSorted === "asc") {
              column.clearSorting();
            } else {
              column.toggleSorting(false);
            }
          },
        },
        {
          label: "Desc",
          icon: "i-lucide-arrow-down-wide-narrow",
          type: "checkbox",
          checked: isSorted === "desc",
          onSelect: () => {
            if (isSorted === "desc") {
              column.clearSorting();
            } else {
              column.toggleSorting(true);
            }
          },
        },
      ],
    },
    () =>
      h(UButton, {
        color: "neutral",
        variant: "ghost",
        label,
        icon: isSorted
          ? isSorted === "asc"
            ? "i-lucide-arrow-up-narrow-wide"
            : "i-lucide-arrow-down-wide-narrow"
          : "i-lucide-arrow-up-down",
        class: "-mx-2.5 data-[state=open]:bg-elevated",
        "aria-label": `Sort by ${
          isSorted === "asc" ? "descending" : "ascending"
        }`,
      })
  );
}

const sorting = ref([
  {
    id: "id",
    desc: false,
  },
]);
</script>

<template>
  <div class="py-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-2xl text-red-800 font-bold">КОНТАКТЫ</h3>
      <UButton
        variant="ghost"
        icon="i-heroicons-user-plus"
        title="Добавить контакт"
        @click="modal = true"
      />
    </div>
    <div class="my-6">
      <UInput
        v-model="search"
        icon="i-heroicons-magnifying-glass"
        placeholder="Поиск по имени или организации"
        type="search"
      />
    </div>
    <UModal
      v-model:open="modal"
      title="Добавить контакт"
      description="Введите данные"
    >
      <template #body>
        <LazyContentPhoneStepper
          :phone="phone"
          :organizations="items"
          @update="
            modal = false;
            phone = {} as Phone;
            refresh();
          "
        />
      </template>
    </UModal>
    <UTable
      v-model:expanded="expanded"
      v-model:sorting="sorting"
      sticky
      class="flex-1 max-h-[800px]"
      :data="phones"
      :columns="columns"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      :loading="status === 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
    >
      <template #expanded="{ row }">
        <ElementsLabelValue
          label="Название организации"
          :value="row.original.organization"
        />
        <ElementsLabelValue label="Полное имя" :value="row.original.fullname" />
        <ElementsLabelValue label="Телефон" :value="row.original.phone" />
        <ElementsLabelValue label="Мобильный" :value="row.original.mobile" />
        <ElementsLabelValue label="Email" :value="row.original.email" />
        <ElementsLabelValue
          label="Комментарий"
          :value="row.original.comments"
        />
        <ElementsLabelValue
          label="Дата записи"
          :value="
            row.original.created
              ? new Date(row.original.created)
                  .toLocaleDateString('ru-RU')
                  .split(',')[0]
              : ''
          "
        />
      </template>
    </UTable>
  </div>
</template>
