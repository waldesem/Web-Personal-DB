<script setup lang="ts">
import type { Persons } from "@/types";

await preloadComponents([
  "DivsPhotoCard",
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
  await authFetch("/route/anketa/self/" + candId.value);
  pending.value = false;
  await refresh();
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
  <div>
    <div class="mb-3">
      <UButton
        :disabled="pending"
        :loading="pending || status === 'pending'"
        :title="
          person.user_id != stateUser.id
            ? 'Назначить анкету на себя'
            : 'Переключить режим редактирования'
        "
        variant="ghost"
        @click="switchSelf"
      >
        <ElementsHeaderDiv
          :header="`${person['surname']} ${person['firstname']} ${
            person['patronymic'] ? person['patronymic'] : ''
          }`"
        />
        <UBadge
          v-if="person.editable"
          :color="person.user_id != stateUser.id ? 'red' : 'green'"
          class="animate-pulse"
        >
          {{
            person.user_id != stateUser.id
              ? "Анкета редактируется другим пользователем"
              : "Анкета редактируется"
          }}
        </UBadge>
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
