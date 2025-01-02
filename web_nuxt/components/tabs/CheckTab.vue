<script setup lang="ts">
import type { Verification } from "@/types";
import { emitMessage } from "@/utils";

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
</script>

<template>
  <UButton
    v-if="editable"
    :loading="status == 'pending' || pending"
    :label="
      status == 'pending' || pending
        ? 'Обновление данных...'
        : 'Добавить запись'
    "
    variant="link"
    @click="modal = !modal"
  />
  <UModal v-model="modal" prevent-close>
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
  <div
    v-for="(item, index) in checks"
    :key="index"
    class="text-sm text-gray-500 dark:text-gray-400 py-1"
  >
    <ElementsCardDiv>
      <template #header>
        <div class="tex-base text-red-800 dark:text-gray-400 font-medium">
          {{ "Проверка кандидата ID #" + item["id"] }}
        </div>
      </template>
      <ElementsLabelSlot
        v-if="item['workplace']"
        :label="'Проверка по местам работы'"
      >
        {{ item["workplace"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['document']" :label="'Проверка паспорта'">
        {{ item["document"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['inn']" :label="'Проверка ИНН'">{{
        item["inn"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['debt']" :label="'Проверка ФССП'">{{
        item["debt"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="item['bankruptcy']"
        :label="'Проверка банкротства'"
      >
        {{ item["bankruptcy"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['bki']" :label="'Проверка БКИ'">{{
        item["bki"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="item['courts']"
        :label="'Проверка судебных решений'"
      >
        {{ item["courts"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="item['affilation']"
        :label="'Проверка аффилированности'"
      >
        {{ item["affilation"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="item['terrorist']"
        :label="'Проверка по списку террористов'"
      >
        {{ item["terrorist"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['mvd']" :label="'Проверка в розыск'">{{
        item["mvd"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="item['internet']"
        :label="'Проверка в открытых источниках'"
      >
        {{ item["internet"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['cronos']" :label="'Проверка Кронос'">
        {{ item["cronos"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot
        v-if="item['addition']"
        :label="'Дополнительная информация'"
      >
        {{ item["addition"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot v-if="item['comment']" :label="'Комментарии'"
        >{{ item["comment"] }}
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Результат'">{{
        item["conclusion"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дата записи'">
        {{ new Date(item["created"]).toLocaleString("ru-RU") }}
      </ElementsLabelSlot>
      <template v-if="editable" #footer>
        <TabMenu
          :item="'checks'"
          @cancel="modal = false"
          @update="
            check = item;
            modal = true;
          "
          @delete="deleteCheck(item['id'], index)"
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
