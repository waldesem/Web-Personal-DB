<script setup lang="ts">
import type { AccordionItem } from "@nuxt/ui";
import type { DivsItems, Persons } from "@/types";

const { $customFetch } = useNuxtApp();

const emits = defineEmits(["refresh"]);

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
const editable = inject("editable") as Ref<boolean>;
const status = inject("status") as Ref<string>;

const person = toRef(props.person as Persons);
const modal = ref(false);

function submitPerson(person_id: string) {
  modal.value = false;
  status.value = "pending";
  emits("refresh");
  if (person_id == person.value.id) {
    makeToast("success", "Информация успешно обновлена");
    status.value = "success";
  } else {
    makeToast();
  }
}

async function deletePerson() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  if (!confirm("Данные будут удалены безвозвратно!?")) return;
  status.value = "pending";
  const { message } = await $customFetch(`/route/items/persons/${person.value.id}`, {
    method: "DELETE",
  }) as Record<string, string>;
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
  { content: "staffs", label: "Должности", icon: "i-lucide-user" },
  {
    content: "educations",
    label: "Образование",
    icon: "i-lucide-graduation-cap",
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-lucide-book-text",
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-lucide-house",
  },
  { content: "contacts", label: "Контакты", icon: "i-lucide-phone-call" },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-lucide-users-round",
  },
];
</script>

<template>
  <div class="mt-4">
    <LazyElementsDivMenu
      v-if="editable"
      @change="modal = true"
      @delete="deletePerson()"
    />
    <div v-if="status == 'pending'" class="ps-2">
      <LazyElementsSkeletonDiv :rows="props.rows" />
    </div>
    <div v-else class="ps-2">
      <LazyItemsPersonItem :item="person" />
    </div>
    <UModal
      v-if="editable"
      v-model:open="modal"
      title="Редактирование анкеты"
      description="Отредактируйте анкетные данные"
    >
      <template #body>
        <LazyFormsResumeForm :resume="person" @update="submitPerson" />
      </template>
    </UModal>
    <USeparator />
    <UAccordion :items="items" :unmount-on-hide="false">
      <template #content="{ item }">
        <ContentSharedView :view="item.content" />
      </template>
    </UAccordion>
  </div>
</template>
