<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Verification } from "@/types/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean;

const checkData = ref({
  collapse: false,
  collapseAdd: false,
  edit: false,
  itemId: "",
  check: {} as Verification,
});

const { refresh, status } = await useLazyAsyncData("checks", async () => {
  await anketaState.getItem("checks");
});

async function updateCheck(checkForm: Verification) {
  closeAction();
  anketaState.updateItem("checks", checkForm);
  refresh();
}

async function deleteCheck(index: string) {
  closeAction();
  anketaState.deleteItem(index, "checks");
  refresh();
}

async function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  checkData.value.edit = false;
  checkData.value.itemId = "";
  checkData.value.collapse = false;
}

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}
</script>

<template>
  <UButton
    v-if="editState"
    class="py-3"
    :label="!checkData.collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="checkData.collapse = !checkData.collapse"
  />
  <Transition name="slide-fade">
    <div v-if="checkData.collapse" class="py-3">
      <UCard>
        <FormsCheckForm @submit="updateCheck" @cancel="cancelOperation" />
      </UCard>
    </div>
  </Transition>
  <div
    v-if="
      anketaState.anketa.value.checks && anketaState.anketa.value.checks.length
    "
  >
    <div
      v-for="(item, index) in anketaState.anketa.value.checks"
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
          v-if="checkData.edit && checkData.itemId == item['id'].toString()"
          :check="checkData.check"
          @cancel="cancelOperation"
          @submit="updateCheck"
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
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            @update="
              checkData.check = item;
              checkData.itemId = item['id'].toString();
              checkData.edit = true;
            "
            @delete="deleteCheck(item['id'])"
            @upload="openFileForm('check-file')"
          />
          <div v-show="false">
            <UInput
              id="check-file"
              type="file"
              accept="*"
              multiple
              @change="
                anketaState.submitFile(
                  $event,
                  'checks',
                  anketaState.share.value.candId
                )
              "
            />
          </div>
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending'" :rows="18" />
    <p v-else class="text-red-800">Проверка кандидата отсутствует</p>
  </div>
</template>
