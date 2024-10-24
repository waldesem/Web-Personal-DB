<script setup lang="ts">
import type { Persons } from "@/types/interfaces";

const authFetch = useFetchAuth();
const userState = useUserState();

const toast = useToast();
const route = useRoute();

const candId = computed(() => route.params.id) as Ref<string>;

const person = ref({} as Persons);

const pending = ref(false);

const { refresh, status } = await useLazyAsyncData("anketa", async () => {
  person.value = (await authFetch(
    "/api/items/persons/" + candId.value
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

const badgeItems = {
  current: {
    label: "Анкета редактируется текущим пользователем",
    color: "green",
  },
  thirdparty: {
    label: "Анкета редактируется другим пользователем",
    color: "red",
  },
  others: {
    label: "Анкета не редактируется пользователями",
    color: "blue",
  },
};

const badge = computed(() => {
  if (person.value["editable"]) {
    if (person.value["user_id"] == userState.value.id) {
      return badgeItems.current;
    } else if (person.value["user_id"] != userState.value.id) {
      return badgeItems.thirdparty;
    }
  }
  return badgeItems.others;
});

const editState = computed(() => {
  return (
    person.value["editable"] &&
    userState.value.role == "user" &&
    userState.value.id == person.value["user_id"]
  );
});

async function switchSelf(): Promise<void> {
  if (!confirm("Вы действительно хотите включить/выключить режим правки")) {
    return;
  }
  pending.value = true;
  await authFetch("/api/self/" + candId.value);
  await refresh();
  pending.value = false;
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
    <DivsPhotoCard
      :cand-id="candId"
      :editable="editState"
      @message="emitMessage"
    />
    <div v-if="userState.role == 'user'" class="relative">
      <div class="absolute bottom-0 right-20">
        <UButton
          :disabled="pending"
          variant="link"
          size="xl"
          @click="switchSelf"
        >
          <div v-if="pending || status === 'pending'">
            <UIcon name="i-heroicons-arrow-path animate-spin w-8 h-8" />
          </div>
          <div v-else class="animate-pulse w-16 h-16" >
            <UBadge :color="(badge.color as any)" variant="solid">
              {{ badge.label }}
            </UBadge>
          </div>
        </UButton>
      </div>
    </div>
    <USkeleton v-if="status  === 'pending'" class="mb-6 h-16 w-96" />
    <ElementsHeaderDiv
      v-else
      :div="'py-3'"
      :header="`${person['surname']} ${person['firstname']} ${
        person['patronymic'] ? person['patronymic'] : ''
      }`"
    />
    <UTabs :items="tabs">
      <template #anketaTab>
        <TabsAnketaTab
          :cand-id="candId"
          :editable="editState"
          :person="person"
          @status="status"
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
