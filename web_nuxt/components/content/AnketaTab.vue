<script setup lang="ts">
import type { AccordionItem } from "@nuxt/ui";

const props = defineProps({
  rows: {
    type: Number,
    required: true,
  },
  person: {
    type: Object as PropType<Persons>,
    required: true,
  },
});

const emits = defineEmits(["refresh"]);

const editable = inject("editable") as Ref<boolean>;
const status = inject("status") as Ref<string>;

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
    emits("refresh");
    makeToast();
  }
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
    return navigateTo("/persons");
  } else {
    makeToast();
    status.value = "error";
  }
}

interface Accordion extends AccordionItem {
  content: DivsItems;
}

const items: Accordion[] = [
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
  <div class="mt-6">
    <LazyElementsDivMenu
      v-if="editable"
      @change="modal = true"
      @delete="deleteItem()"
    />
    <div v-if="status == 'pending'" class="ps-2">
      <ElementsSkeletonDiv :rows="props.rows" />
    </div>
    <div v-else class="ps-2">
      <ItemsPersonItem :item="person" />
    </div>
    <UModal
      v-if="editable"
      v-model:open="modal"
      title="Редактирование анкеты"
      description="Отредактируйте анкетные данные"
    >
      <template #body>
        <LazyFormsResumeForm :resume="person" @update="submitResume" />
      </template>
    </UModal>
    <USeparator />
    <UAccordion :items="items" :unmount-on-hide="false">
      <template #content="{ item }">
        <ContentSharedView :rows="3" :view="(item.content as DivsItems)" />
      </template>
    </UAccordion>
  </div>
</template>
