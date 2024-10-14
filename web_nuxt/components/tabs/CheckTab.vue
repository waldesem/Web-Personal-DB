<script setup lang="ts">
import type { Verification } from "@/types/interfaces";
import { useDateFormat } from "@vueuse/core";

prefetchComponents(["FormsCheckForm", "ElementsSkeletonDiv"]);

const authFetch = useFetchAuth();

const toast = useToast();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const edit = ref(false);
const pending = ref(false);
const collapse = ref(false);
const itemId = ref("");
const check = ref({} as Verification);

const {
  data: checks,
  refresh,
  status,
} = await useLazyAsyncData("checks", async () => {
  const response = await authFetch(`/api/checks/${props.candId}`);
  return response as Verification[];
});

async function submitCheck(form: Verification) {
  pending.value = true;
  closeAction();
  await authFetch("/api/checks/" + props.candId, {
    method: "POST",
    body: form,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  pending.value = false;
  await refresh();
}

async function deleteCheck(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  await authFetch(`/api/checks/${id}`, {
    method: "DELETE",
  });
  toast.add({
    icon: "i-heroicons-information-circle",
    title: "Информация",
    description: `Запись с ID ${id} удалена`,
    color: "primary",
  });
  await refresh();
}

function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="props.editable"
    class="py-3"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsCheckForm
          :cand-id="props.candId"
          @update="submitCheck"
          @cancel="cancelOperation"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="checks && checks.length">
    <div
      v-for="(item, index) in checks"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="18" />
      <ElementsCardDiv v-else>
        <template #header>
          <div class="tex-base text-red-800 dark:text-gray-400 font-medium">
            {{ "Проверка кандидата ID #" + item["id"] }}
          </div>
        </template>
        <FormsCheckForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :check="item"
          @cancel="cancelOperation"
          @update="submitCheck"
        />
        <div v-else>
          <ElementsLabelSlot
            v-if="item['workplace']"
            :label="'Проверка по местам работы'"
          >
            {{ item["workplace"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot
            v-if="item['document']"
            :label="'Проверка паспорта'"
          >
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
          <ElementsLabelSlot v-if="item['cronos']" :label="'Проверка в Кронос'">
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
          <ElementsLabelSlot :label="'Сотрудник'">{{
            item["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{ useDateFormat(item["created"], "YYYY-MM-DD HH:mm:ss") }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :cand-id="props.candId"
            :item="'checks'"
            @update="
              check = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @delete="deleteCheck(item['id'])"
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="18" />
    <p v-else class="text-red-800">Проверка кандидата отсутствует</p>
  </div>
</template>
