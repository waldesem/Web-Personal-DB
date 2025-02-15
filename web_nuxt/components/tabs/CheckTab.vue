<script setup lang="ts">
import type { Verification } from "@/types";

prefetchComponents("FormsCheckForm");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const check = ref({} as Verification);
const checks = ref<Verification[]>([]);

const { refresh, status } = await useLazyAsyncData("checks", async () => {
  checks.value = (await authFetch(
    `/route/items/checks/${candId.value}`
  )) as Verification[];
});

async function submitCheck(form: Verification) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/checks/${candId.value}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  check.value = {} as Verification;
  await refresh();
  emitMessage(message);
}

async function deleteCheck(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/checks/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    checks.value.splice(idx, 1);
  }
  emitMessage(message);
}

const items = computed(() =>
  checks.value.map((item, _) => ({
    label: "Проверка кандидата ID #" + item["id"],
    defaultOpen: true,
    description: item,
  }))
);
</script>

<template>
  <div v-if="editable || status == 'pending'" class="my-1">
    <UButton
      :loading="status == 'pending' || pending"
      :label="
        status == 'pending' || pending
          ? 'Обновление данных...'
          : 'Добавить запись'
      "
      variant="link"
      @click="modal = !modal"
    />
  </div>
  <UModal v-model="modal" prevent-close :ui="{ width: 'sm:max-w-4xl' }">
    <ElementsCardDiv>
      <FormsCheckForm
        :check="check"
        @cancel="
          check = {} as Verification;
          modal = false;
        "
        @update="submitCheck"
      />
    </ElementsCardDiv>
  </UModal>
  <UAccordion :items="items" size="lg" multiple>
    <template #item="{ item, index }">
      <ElementsCardDiv>
        <ElementsLabelSlot
          v-if="item.description.workplace"
          :label="'Проверка по местам работы'"
        >
          {{ item.description.workplace }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.document"
          :label="'Проверка паспорта'"
        >
          {{ item.description.document }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.inn"
          :label="'Проверка ИНН'"
          >{{ item.description.inn }}</ElementsLabelSlot
        >
        <ElementsLabelSlot
          v-if="item.description.debt"
          :label="'Проверка ФССП'"
          >{{ item.description.debt }}</ElementsLabelSlot
        >
        <ElementsLabelSlot
          v-if="item.description.bankruptcy"
          :label="'Проверка банкротства'"
        >
          {{ item.description.bankruptcy }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.bki"
          :label="'Проверка БКИ'"
          >{{ item.description.bki }}</ElementsLabelSlot
        >
        <ElementsLabelSlot
          v-if="item.description.courts"
          :label="'Проверка судебных решений'"
        >
          {{ item.description.courts }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.affilation"
          :label="'Проверка аффилированности'"
        >
          {{ item.description.affilation }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.terrorist"
          :label="'Проверка по списку террористов'"
        >
          {{ item.description.terrorist }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.mvd"
          :label="'Проверка в розыск'"
          >{{ item.description.mvd }}</ElementsLabelSlot
        >
        <ElementsLabelSlot
          v-if="item.description.internet"
          :label="'Проверка в открытых источниках'"
        >
          {{ item.description.internet }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.cronos"
          :label="'Проверка Кронос'"
        >
          {{ item.description.cronos }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.addition"
          :label="'Дополнительная информация'"
        >
          {{ item.description.addition }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item.description.comment"
          :label="'Комментарии'"
          >{{ item.description.comment }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Результат'">
          <UBadge
            :color="
              item.description.conclusion === 'СОГЛАСОВАНО'
                ? 'green'
                : item.description.conclusion === 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'
                ? 'primary'
                : 'red'
            "
            :label="item.description.conclusion"
            variant="solid"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item.description.created).toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
        <template v-if="editable" #footer>
          <ElementsTabMenu
            :item="'checks'"
            @cancel="modal = false"
            @update="
              check = item.description;
              modal = true;
            "
            @delete="deleteCheck(item.description.id, index)"
          />
        </template>
      </ElementsCardDiv>
    </template>
  </UAccordion>
</template>
