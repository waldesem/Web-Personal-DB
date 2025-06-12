<script setup lang="ts">
import { watchDebounced } from "@vueuse/core";
import type { TableColumn } from "@nuxt/ui";
import type { Phone } from "@/types";

const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");

const search = ref("");
const phones = ref([] as Phone[]);
const phone = ref([] as Phone[]);
const modal = ref(false);
const expanded = ref({ 1: false });

const { refresh, status } = await useLazyAsyncData("users", async () => {
  const data = (await fetchAuth("/route/phones", {
    params: {
      search: search.value,
    },
  })) as Phone[];
  phones.value = data;
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

function getRowItems(phone: Phone) {
  return [
    {
      label: "Удалить",
      onSelect() {
        deletePhone(phone.id);
      },
    },
    {
      label: "Изменить",
      onSelect() {},
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
  { accessorKey: "organization", header: "Организация" },
  { accessorKey: "fullname", header: "Полное имя" },
  { accessorKey: "phone", header: "Телефон" },
  { accessorKey: "created", header: "Дата" },
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
</script>

<template>
  <div>
    <div class="py-4">
      <h3 class="text-2xl text-red-800 font-bold">КОНТАКТЫ</h3>
    </div>
    <UInput
      v-model="search"
      icon="i-heroicons-magnifying-glass"
      placeholder="Поиск по имени или организации"
      type="search"
    />
    <div class="flex items-center justify-between my-4">
      <UButton variant="link" label="Добавить контакт" @click="modal = true" />
    </div>
    <UModal
      v-model:open="modal"
      title="Добавить контакт"
      description="Введите данные"
    >
      <template #body>
        <LazyPhoneForm
          :phone="phone"
          @update="
            modal = false;
            refresh();
          "
        />
      </template>
    </UModal>

    <UTable
      v-model:expanded="expanded"
      sticky
      class="flex-1 max-h-[640px]"
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
        <ElementsLabelValue label="Город" :value="row.original.city" />
        <ElementsLabelValue label="Полное имя" :value="row.original.fullname" />
        <ElementsLabelValue label="Телефон" :value="row.original.phone" />
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
