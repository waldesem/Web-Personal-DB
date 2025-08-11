<script setup lang="ts">
import type { AccordionItem } from "@nuxt/ui";
import type {
  Address,
  Affilation,
  Contact,
  DivsItems,
  Education,
  Passport,
  Persons,
  Previous,
  Staff,
  Work,
} from "@/types";

const { $api } = useNuxtApp();

const emits = defineEmits(["refresh"]);

const props = defineProps({
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
  const { message } = await $api<Record<string, string>>(
    `/route/persons/${person.value.id}`,
    {
      method: "DELETE",
    }
  );
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

const items = [
  {
    content: "staffs",
    label: "Должности",
    icon: "i-lucide-user",
    slot: "staffs" as const,
  },
  {
    content: "educations",
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations" as const,
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces" as const,
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents" as const,
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses" as const,
  },
  {
    content: "contacts",
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts" as const,
  },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous" as const,
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations" as const,
  },
] satisfies Accordion[];
</script>

<template>
  <div class="mt-4">
    <LazyElementsDivMenu
      v-if="editable"
      @change="modal = true"
      @delete="deletePerson()"
    />
    <div v-if="status == 'pending'" class="ps-2">
      <LazyElementsSkeletonDiv :rows="12" />
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
      <template #staffs="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <ItemsStaffItem :item="itemContent as Staff" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsStaffForm :item="formContent as Staff" @update="submitItem" />
          </template>
        </ContentSharedView>
      </template>

      <template #educations="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <ItemsEducationItem :item="itemContent as Education" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsEducationForm
              :item="formContent as Education"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #workplaces="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <ItemsWorkplaceItem :item="itemContent as Work" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsWorkplaceForm
              :item="formContent as Work"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #documents="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <ItemsDocumentItem :item="itemContent as Passport" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsDocumentForm
              :item="formContent as Passport"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #addresses="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <ItemsAddressItem :item="itemContent as Address" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsAddressForm
              :item="formContent as Address"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #contacts="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <ItemsContactItem :item="itemContent as Contact" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsContactForm
              :item="formContent as Contact"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #previous="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <ItemsPreviousItem :item="itemContent as Previous" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsPreviousForm
              :item="formContent as Previous"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <template #affilations="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <ItemsAffilationItem :item="itemContent as Affilation" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsAffilationForm
              :item="formContent as Affilation"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>
    </UAccordion>
  </div>
</template>
