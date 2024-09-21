<script setup lang="ts">
import type { Verification } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

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
  refresh();
}

async function cancelOperation() {
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
      <UCard>
        <FormsCheckForm
          :cand-id="props.candId"
          @update="refresh"
          @cancel="cancelOperation"
          @close="closeAction"
        />
      </UCard>
    </div>
  </Transition>
  <div v-if="checks && checks.length">
    <div
      v-for="(item, index) in checks"
      :key="index"
      class="text-sm text-gray-500 dark:text-gray-400 py-1"
    >
      <ElementsSkeletonDiv v-if="status == 'pending'" :rows="18" />
      <UCard v-else>
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
          @close="closeAction"
          @update="refresh"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Проверка по местам работы'">
            {{ item["workplace"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка паспорта'">
            {{ item["document"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка ИНН'">{{
            item["inn"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка ФССП'">{{
            item["debt"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка банкротства'">
            {{ item["bankruptcy"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка БКИ'">{{
            item["bki"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка судебных решений'">
            {{ item["courts"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка аффилированности'">
            {{ item["affilation"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка по списку террористов'">
            {{ item["terrorist"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка в розыск'">{{
            item["mvd"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка в открытых источниках'">
            {{ item["internet"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка в Кронос'">
            {{ item["cronos"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дополнительная информация'">
            {{ item["addition"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Комментарии'"
            >{{ item["comment"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Результат'">{{
            item["conclusion"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            item["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :cand-id="props.candId"
            :input-id="'checks-file'"
            :item="'checks'"
            @update="
              check = item;
              itemId = item['id'].toString();
              edit = true;
            "
            @delete="deleteCheck(item['id'])"
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending'" :rows="18" />
    <p v-else class="text-red-800">Проверка кандидата отсутствует</p>
  </div>
</template>
