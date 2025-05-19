<script setup lang="ts">
import type { AccordionItem } from "@nuxt/ui";
import type { Persons } from "@/types";

await preloadComponents(["DivsSharedDiv"]);
await preloadComponents("ItemsSharedDiv");

const props = defineProps({
  person: {
    type: Object as PropType<Persons>,
    required: true,
  },
});

const emits = defineEmits(["refresh"]);

const editable = inject("editable") as Ref<boolean>;
const status = inject("status") as Ref<String>;

const modal = ref(false);

async function submitResume(form: Persons) {
  modal.value = false;
  status.value = "pending";
  const { message } = (await fetchAuth("/route/items/persons", {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  if (message == "success") {
    makeToast(message, "Информация успешно обновлена");
  } else {
    makeToast();
  }
  emits("refresh");
}

async function deleteItem() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  if (!confirm("Данные будут удалены безвозвратно!?")) return;
  status.value = "pending";
  const { message } = (await fetchAuth(
    `/route/items/persons/${props.person.id}`,
    {
      method: "DELETE",
    }
  )) as Record<string, string>;
  if (message == "success") {
    makeToast(message, "Информация успешно обновлена");
    await navigateTo("/persons");
  } else {
    makeToast();
    status.value = "error";
  }
}

const items: AccordionItem[] = [
  { content: "staffs", label: "Должности", icon: "i-heroicons-user" },
  {
    content: "educations",
    label: "Образование",
    icon: "i-heroicons-academic-cap",
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-heroicons-briefcase",
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-heroicons-document",
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-heroicons-home",
  },
  { content: "contacts", label: "Контакты", icon: "i-heroicons-phone" },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-heroicons-pencil-square",
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-heroicons-users",
  },
];
</script>

<template>
  <div v-if="editable" class="relative">
    <div class="absolute top-2 right-2">
      <UDropdownMenu
        :items="[
          {
            label: 'Изменить',
            icon: 'i-heroicons-pencil-square',
            onSelect() {
              modal = true;
            },
          },
          {
            label: 'Удалить',
            icon: 'i-heroicons-trash',
            onSelect() {
              deleteItem();
            },
          },
        ]"
        :content="{ align: 'end' }"
      >
        <UButton
          :loading="status == 'pending'"
          size="xl"
          color="neutral"
          icon="i-heroicons-ellipsis-vertical"
          variant="ghost"
          title="Выбор действия"
        />
      </UDropdownMenu>
    </div>
  </div>
  <div v-if="!person.id" class="ps-2">
    <div
      v-for="p in Object.keys(person)"
      :key="p"
      class="flex grid grid-cols-12 gap-3 mb-3"
    >
      <div class="col-span-3">
        <USkeleton class="h-4" />
      </div>
      <div class="col-span-9">
        <USkeleton class="h-4 w-[300px]" />
      </div>
    </div>
  </div>
  <div v-else class="ps-2">
    <ItemsSharedItem :view="'person'" :item="person" />
  </div>
  <UModal 
    v-if="editable" 
    v-model:open="modal"
    :dismissible="false"
    title="Анкетные данные"
    description="Данные профиля"
  >
    <template #content>
      <div class="m-4">
        <FormsResumeForm
          :resume="person"
          @update="submitResume"
          @cancel="modal = false"
        />
      </div>
    </template>
  </UModal>
  <USeparator />
  <UAccordion :items="items" :unmount-on-hide="false">
    <template #content="{ item }">
      <ItemsSharedDiv :view="(item.content as string)" />
    </template>
  </UAccordion>
</template>
