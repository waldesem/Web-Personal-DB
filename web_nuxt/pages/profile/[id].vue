<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { TabsItem } from "@nuxt/ui";
import type {
  Inquisition,
  Needs,
  Persons,
  Pfo,
  Verification,
} from "@/types";

// Презагрузка компонентов
await preloadComponents(["ContentAnketaTab", "ContentSharedView"]);

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем композаблы для работы с данными
const route = useRoute();
const userState = useStateUser();

// Получаем данные id кандидата из URL
const candId = computed(() => route.params.id as string);
// Передаем данные id кандидата в другие компоненты
provide("candId", candId);

// Определяем функцию для получения данных из API
const { data, status, refresh } = await useAsyncData("persons", async () => {
  return (await $api("/route/persons/" + candId.value)) as Persons;
});

// Вычисляем статус редактирования анкеты
const editable = computed(() => {
  return (
    data.value &&
    data.value.editable &&
    userState.value.role == "user" &&
    userState.value.id == data.value.user_id
  );
});
// Передаем статус редактирования в другие компоненты
provide("editable", editable);

// Определяем функцию для переключения режима редактирования
async function switchSelf(): Promise<void> {
  if (data.value && data.value.user_id != userState.value.id) {
    if (data.value.editable) {
      if (
        !confirm(
          "Анкета редактируется другим пользователем. Переключить режим?"
        )
      ) {
        return;
      }
    } else if (!confirm("Вы хотите назначить анкету на себя?")) {
      return;
    }
  } else if (!confirm("Переключить режим редактирования?")) {
    return;
  }
  status.value = "pending";
  const { message } = await $api<Record<string, string>>(
    "/route/self/" + data.value?.id
  );
  status.value = message as "success" | "error";
  if (message == "success") {
    await refresh();
  } else {
    useToasts();
  }
}

// Определяем диалог загрузки файлов
const { open, onChange } = useFileDialog();

// Определяем функцию для загрузки файлов
onChange(async (files) => {
  if (!files) return;
  const formData = new FormData();
  for (const file of files) {
    if (file.size > 10 * 1024 * 1024) {
      useToasts("info", "Размер одного файла не должен превышать 10 МБ");
      continue;
    }
    formData.append("file", file);
  }
  const { message } = await $api<Record<string, string>>(
    `/route/files/${candId.value}`,
    {
      method: "POST",
      body: formData,
    }
  );
  status.value = message as "success" | "error";
  if (message == "success") {
    useToasts(message, "Файлы успешно загружены");
  } else {
    useToasts();
  }
});

// Определяем массив элементов табов
const items = [
  {
    label: "Анкета",
    icon: "i-lucide-user",
    slot: "person" as const,
  },
  {
    label: "Проверки",
    icon: "i-lucide-circle-check-big",
    slot: "checks" as const,
  },
  {
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as const,
  },
  {
    label: "Расследования",
    icon: "i-lucide-briefcase-business",
    slot: "investigations" as const,
  },
  {
    label: "Запросы",
    icon: "i-lucide-book-text",
    slot: "inquiries" as const,
  },
] satisfies TabsItem[];
</script>

<template>
  <div>
    <div class="flex items-center justify-between py-4">
      <!-- Выводим скелетный элемент. если данные ещё не загружены -->
      <USkeleton v-if="status == 'pending'" class="py-1 h-10 w-96" />
      <!-- Заголовок -->
      <div v-else class="py-1">
        <h3 class="text-2xl text-red-800 font-bold">
          {{ `${data?.surname} ${data?.firstname} ${data?.patronymic ?? ""}` }}
        </h3>
      </div>

      <!-- Кнопки для загрузки файлов и переключения режима редактирования -->
      <div v-if="userState.role == 'user'" class="flex items-center space-x-4">
        <UButton
          :loading="status === 'pending'"
          variant="outline"
          icon="i-lucide-cloud-upload"
          label="Загрузить файлы"
          @click="open()"
        />
        <UButton
          :loading="status === 'pending'"
          :color="
            !data?.editable
              ? 'secondary'
              : data.user_id == userState.id
              ? 'success'
              : 'error'
          "
          :label="
            !data?.editable
              ? 'Доступно  для редактирования'
              : data.user_id == userState.id
              ? 'Назначено текущему пользователю'
              : 'Редактируется другим пользователем'
          "
          @click="switchSelf"
        />
      </div>
    </div>
    <!-- Меню для переключения между вкладками -->
    <UTabs
      :unmount-on-hide="false"
      color="info"
      :items="items"
      variant="pill"
      class="gap-4 w-full"
      :ui="{ trigger: 'flex-1' }"
    >
      <!-- Вкладка для отображения анкеты -->
      <template #person>
        <ContentAnketaTab :person="(data ?? {} as Persons)" :status="status" />
      </template>

      <!-- Вкладка для отображения проверок -->
      <template #checks="{ item }">
        <ContentSharedView :view="item.slot" :rows="16">
          <!-- Отображаем элементы проверки -->
          <template #item="{ itemContent }">
            <ItemsCheckItem :item="(itemContent as Verification)" />
          </template>

          <!-- Отображаем форму проверки -->
          <template #form="{ formContent, submitItem }">
            <FormsCheckForm
              :item="(formContent as Verification)"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <!-- Вкладка для отображения полиграфов -->
      <template #poligrafs="{ item }">
        <ContentSharedView :view="item.slot" :rows="4">
          <template #item="{ itemContent }">
            <ItemsPoligrafItem :item="(itemContent as Pfo)" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsPoligrafForm
              :item="(formContent as Pfo)"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <!-- Вкладка для отображения расследований -->
      <template #investigations="{ item }">
        <ContentSharedView :view="item.slot" :rows="3">
          <template #item="{ itemContent }">
            <ItemsInquestItem :item="(itemContent as Inquisition)" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsInquestForm
              :item="(formContent as Inquisition)"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>

      <!-- Вкладка для отображения запросов -->
      <template #inquiries="{ item }">
        <ContentSharedView :view="item.slot" :rows="3">
          <template #item="{ itemContent }">
            <ItemsInquiryItem :item="(itemContent as Needs)" />
          </template>

          <template #form="{ formContent, submitItem }">
            <FormsInquiryForm
              :item="(formContent as Needs)"
              @update="submitItem"
            />
          </template>
        </ContentSharedView>
      </template>
    </UTabs>
  </div>
</template>
