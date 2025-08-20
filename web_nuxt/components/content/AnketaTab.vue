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

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем данные которые передаются из родительского компонента
const props = defineProps({
  person: {
    type: Object as PropType<Persons>,
    required: true,
  },
  status: {
    type: String as PropType<"idle" | "pending" | "success" | "error">,
    default: "success",
  },
});

// Преобразуем переменную для чтения в реактивную
const status = toRef(props.status);

// Инжектируем данные (находится ли анкета в режиме редактирования)
const editable = inject("editable") as Ref<boolean>;

// Объявляем переменную для переключения модального окна
const modal = ref(false);

// Определяем функцию для отправки данных формы на сервер
function submitPerson(person_id: number | null) {
  modal.value = false;
  if (person_id) {
    status.value = "pending";
    refreshNuxtData("persons");
    useToasts("success", "Информация успешно обновлена");
    status.value = "success";
  } else {
    useToasts();
  }
}

// Определяем функцию для удаления данных
async function deletePerson() {
  if (!confirm("Вы действительно хотите удалить профиль и связанные записи?"))
    return;
  if (!confirm("Все данные будут удалены безвозвратно!?")) return;
  status.value = "pending";
  const { message } = await $api<Record<string, string>>(
    `/route/persons/${props.person.id}`,
    {
      method: "DELETE",
    }
  );
  if (message == "success") {
    useToasts(message, "Информация успешно обновлена");
    return navigateTo("/persons");
  } else {
    useToasts();
    status.value = "error";
  }
}

// Определяем интерфейс для элементов аккордеона
interface Accordion extends AccordionItem {
  content: DivsItems;
}

// Определяем массив элементов аккордеона
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
    <!-- Выводим кнопки редактирования или удаления данных если доступно редактирование -->
    <LazyElementsDivMenu
      v-if="editable"
      @update="modal = true"
      @refresh="deletePerson()"
    />

    <!-- Выводим скелетный элемент. если данные ещё не загружены -->
    <div v-if="status == 'pending'" class="ps-2">
      <LazyElementsSkeletonDiv :rows="12" />
    </div>
    <!-- Выводим элемент данных -->
    <div v-else class="ps-2">
      <LazyItemsPersonItem :item="props.person" />
    </div>

    <!-- Выводим модальное окно для редактирования данных -->
    <UModal
      v-if="editable"
      v-model:open="modal"
      title="Редактирование анкеты"
      description="Отредактируйте анкетные данные"
    >
      <template #body>
        <!-- Выводим форму для редактирования данных внутри модального окна -->
        <LazyFormsResumeForm :resume="props.person" @update="submitPerson" />
      </template>
    </UModal>

    <USeparator />

    <!-- Выводим аккордеон с данными staffs, educations и т.д. -->
    <UAccordion :items="items" :unmount-on-hide="false">
      <!-- Элемент staffs -->
      <template #staffs="{ item }">
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <!-- Выводим элементы staffs в слоте item -->
            <ItemsStaffItem :item="itemContent as Staff" />
          </template>

          <template #form="{ formContent, submitItem }">
            <!-- Выводим форму для редактирования staffs в слоте form -->
            <FormsStaffForm
              :item="(formContent as Staff)"
              @update="submitItem"
            />
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
              :item="(formContent as Education)"
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
              :item="(formContent as Work)"
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
              :item="(formContent as Passport)"
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
              :item="(formContent as Address)"
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
              :item="(formContent as Contact)"
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
              :item="(formContent as Previous)"
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
              :item="(formContent as Affilation)"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>
    </UAccordion>
  </div>
</template>
