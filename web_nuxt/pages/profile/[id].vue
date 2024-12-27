<script setup lang="ts">
import type { Persons } from "@/types";

await preloadComponents([
  "TabsAnketaTab",
  "TabsCheckTab",
  "TabsPoligrafTab",
  "TabsInvestigateTab",
  "TabsInquiryTab",
]);

const authFetch = useFetchAuth();

const toast = useToast();
const route = useRoute();

const candId = computed(() => route.params.id) as Ref<string>;

const person = ref({} as Persons);
const pending = ref(false);

const { refresh, status } = await useLazyAsyncData("anketa", async () => {
  person.value = (await authFetch(
    "/route/items/persons/" + candId.value
  )) as Persons;
});

const tabs = [
  {
    slot: "anketaTab",
    label: "Анкета",
    icon: "i-heroicons-user",
  },
  {
    slot: "checkTab",
    label: "Проверки",
    icon: "i-heroicons-check-circle",
  },
  {
    slot: "poligrafTab",
    label: "Полиграф",
    icon: "i-heroicons-bolt",
  },
  {
    slot: "investigateTab",
    label: "Расследования",
    icon: "i-heroicons-briefcase",
  },
  {
    slot: "inquiryTab",
    label: "Запросы",
    icon: "i-heroicons-document-text",
  },
];

const editState = computed(() => {
  return (
    person.value["editable"] &&
    stateUser.value.role == "user" &&
    stateUser.value.id == person.value["user_id"]
  );
});

async function switchSelf(): Promise<void> {
  if (person.value.user_id != stateUser.value.id) {
    if (!confirm("Вы хотите назначить анкету на себя?")) {
      return;
    }
  } else if (!confirm("Переключить режим редактирования?")) {
    return;
  }
  pending.value = true;
  const { message } = await authFetch("/route/anketa/self/" + candId.value);
  pending.value = false;
  emitMessage(message):
  if (message == "success") {
    person.value.editable = !person.value.editable;
    person.value.user_id = stateUser.value.id;
}

function emitMessage(message: string) {
  if (message == "success") {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Информация",
      description: "Информация обновлена",
      color: "primary",
    });
  } else {
    toast.add({
      icon: "i-heroicons-exclamation-triangle",
      title: "Внимание",
      description: "Ошибка обновления информации",
      color: "red",
    });
  }
}
</script>

<template>
  <div class="mb-6">
    <div class="mb-3">
      <USkeleton v-if="status === 'pending'" class="my-6 h-8 w-1/3" />
      <ElementsHeaderDiv
        v-else
        :header="`${person['surname']} ${person['firstname']} ${
            person['patronymic'] ? person['patronymic'] : ''
          }`"
      />
      <UButton
        :disabled="pending"
        :loading="pending || status === 'pending'"
        @click="switchSelf"
        size="md"
        :color="!person.editable" ? 'blue' : person.user_id != stateUser.id ? 'red' : 'green'"
        >
          {{
            !person.editable ? "Анкета доступна для редактирования" : person.user_id != stateUser.id
              ? "Анкета редактируется другим пользователем"
              : "Анкета редактируется"
          }}
      </UButton>
    </div>
    <UTabs :items="tabs">
      <template #anketaTab>
        <TabsAnketaTab
          :cand-id="candId"
          :editable="editState"
          :person="person"
          :status="status"
          @message="emitMessage"
          @update="refresh()"
        />
      </template>
      <template #checkTab>
        <TabsCheckTab
          :cand-id="candId"
          :editable="editState"
          @message="emitMessage"
        />
      </template>
      <template #poligrafTab>
        <TabsPoligrafTab
          :cand-id="candId"
          :editable="editState"
          @message="emitMessage"
        />
      </template>
      <template #investigateTab>
        <TabsInvestigateTab
          :cand-id="candId"
          :editable="editState"
          @message="emitMessage"
        />
      </template>
      <template #inquiryTab>
        <TabsInquiryTab
          :cand-id="candId"
          :editable="editState"
          @message="emitMessage"
        />
      </template>
    </UTabs>
  </div>
</template>
