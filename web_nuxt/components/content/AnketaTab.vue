<script setup lang="ts">
import type { Persons } from "@/types";

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
    `/routes/persons/${props.person.id}`,
    {
      method: "DELETE",
    }
  );
  if (message == "success") {
    useToasts(message, "Информация успешно удалена");
    clearNuxtData();
    return navigateTo("/persons");
  } else {
    useToasts();
    status.value = "error";
  }
}

// Определяем массив элементов аккордеона
const items = [
  {
    content: "staffs",
    label: "Должности",
    icon: "i-lucide-user",
    slot: "staffs" as const,
    ItemComponent: resolveComponent("ItemsStaffItem"),
    FormComponent: resolveComponent("FormsStaffItem") 
  },
  {
    content: "educations",
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations" as const,
    ItemComponent: resolveComponent("ItemsEducationItem"),
    FormComponent: resolveComponent("FormsEducationForm"),
  },
  {
    content: "workplaces",
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces" as const,
    ItemComponent: resolveComponent("ItemsWorkplaceItem"),
    FormComponent: resolveComponent("FormsWorkplaceForm"),
  },
  {
    content: "documents",
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents" as const,
    ItemComponent: resolveComponent("ItemsDocumentItem"),
    FormComponent: resolveComponent("FormsDocumentForm"),
  },
  {
    content: "addresses",
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses" as const,
    ItemComponent: resolveComponent("ItemsAddressItem"),
    FormComponent: resolveComponent("FormsAddressForm"),
  },
  {
    content: "contacts",
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts" as const,
    ItemComponent: resolveComponent("ItemsContactItem"),
    FormComponent: resolveComponent("FormsContactForm"),
  },
  {
    content: "previous",
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous" as const,
    ItemComponent: resolveComponent("ItemsPreviousItem"),
    FormComponent: resolveComponent("FormsPreviousForm"),
  },
  {
    content: "affilations",
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations" as const,
    ItemComponent: resolveComponent("ItemsAffilationItem"),
    FormComponent: resolveComponent("FormsAffilationForm"),
  },
];
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
      <template
        v-for="accord in items"
        #[accord.slot]="{ item }"
        :key="accord.slot"
      >
        <ContentSharedView :view="item.content">
          <template #item="{ itemContent }">
            <component
              :is="accord.ItemComponent"
              :item="(itemContent as unknown as undefined)"
            />
          </template>

          <template #form="{ formContent, submitItem }">
            <component
              :is="accord.FormComponent"
              :item="(formContent as unknown as undefined)"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>
    </UAccordion>
  </div>
</template>
