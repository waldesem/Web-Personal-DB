<script setup lang="ts">
import { getPaginationRowModel } from "@tanstack/vue-table";
import type { TableColumn } from "@nuxt/ui";
import type { Phone } from "@/types";

prefetchComponents(["ElementsLabelValue"]);

const UBadge = resolveComponent("UBadge");
const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");
const table = useTemplateRef("table");

const items = ref([] as string[]);
const phones = shallowRef([] as Phone[]);
const phone = ref({} as Phone);
const modal = ref(false);
const expanded = ref({ 1: false });
const globalFilter = ref("");
const pagination = ref({
  pageIndex: 0,
  pageSize: 10,
});

const { refresh, status } = await useLazyAsyncData("users", async () => {
  const { results, organizations } = (await fetchAuth(
    "/route/phones"
  )) as Record<string, unknown> as {
    results: Phone[];
    organizations: string[];
  };
  phones.value = results;
  items.value = organizations;
});

async function submitForm(form: Phone) {
  const { message } = (await fetchAuth("/route/phones", {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  modal.value = false;
  phone.value = {} as Phone;
  await refresh();
  if (message === "success") {
    makeToast("success", "Контакт успешно добавлен/обновлен");
  } else {
    makeToast();
  }
}

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
    {
      label: "Обновить дату",
      onSelect() {
        submitForm(item);
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
        icon: "i-lucide-chevron-down",
        square: true,
        ui: {
          leadingIcon: [
            "transition-transform",
            row.getIsExpanded() ? "duration-200 rotate-180" : "",
          ],
          class: "flex items-center justify-center",
        },
        onClick: () => row.toggleExpanded(),
      }),
  },
  {
    accessorKey: "organization",
    header: "Организация",
  },
  { accessorKey: "fullname", header: "Полное имя" },
  { accessorKey: "phone", header: "Телефон" },
  {
    accessorKey: "created",
    header: "Обновлено",
    cell: ({ row }) => {
      return h(UBadge, {
        color:
          new Date().getTime() - new Date(row.original.created).getTime() <
          365 * 24 * 60 * 60 * 1000
            ? "success"
            : new Date().getTime() - new Date(row.original.created).getTime() <
              365 * 24 * 60 * 60 * 1000 * 3
            ? "primary"
            : "error",
        label: new Date(row.original.created).toLocaleDateString("ru-RU"),
      });
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
              icon: "i-lucide-ellipsis-vertical",
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
  <div class="py-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-2xl text-red-800 font-bold">КОНТАКТЫ</h3>
      <UButton
        variant="ghost"
        icon="i-lucide-user-plus"
        size="lg"
        title="Добавить контакт"
        @click="modal = true"
      />
    </div>
    <div class="my-6">
      <UInput
        v-model="globalFilter"
        icon="i-lucide-search"
        placeholder="Поиск контактов"
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
          @update="submitForm"
        />
      </template>
    </UModal>
    <UTable
      ref="table"
      v-model:expanded="expanded"
      v-model:global-filter="globalFilter"
      v-model:pagination="pagination"
      :pagination-options="{
        getPaginationRowModel: getPaginationRowModel(),
      }"
      :data="phones"
      :columns="columns"
      :meta="{ class: { tr: 'cursor-pointer' } }"
      :loading="status === 'pending'"
      loading-animation="carousel"
      empty="Данные не найдены"
    >
      <template #expanded="{ row }">
        <UCard>
          <ElementsLabelValue
            label="Название организации"
            :value="row.original.organization"
          />
          <ElementsLabelValue
            label="Полное имя"
            :value="row.original.fullname"
          />
          <ElementsLabelValue label="Телефон" :value="row.original.phone" />
          <ElementsLabelValue label="Мобильный" :value="row.original.mobile" />
          <ElementsLabelValue label="Email" :value="row.original.email" />
          <ElementsLabelValue
            label="Комментарий"
            :value="row.original.comments"
          />
        </UCard>
      </template>
    </UTable>
    <div class="flex justify-center border-t border-default py-4">
      <UPagination
        :default-page="
          (table?.tableApi?.getState().pagination.pageIndex || 0) + 1
        "
        :items-per-page="table?.tableApi?.getState().pagination.pageSize"
        :total="table?.tableApi?.getFilteredRowModel().rows.length"
        :sibling-count="1"
        @update:page="(p) => table?.tableApi?.setPageIndex(p - 1)"
      />
    </div>
  </div>
</template>
