<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Verification } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const checkData = ref({
  collapse: false,
  collapseAdd: false,
  edit: false,
  itemId: "",
  check: {} as Verification,
});

function cancelAction() {
  checkData.value.edit = false;
  checkData.value.itemId = "";
  checkData.value.collapse = false;
}

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}

function createElement(jsonList: Array<object>) {
  let divs = "";
  for (const json of jsonList) {
    let table = "";
    for (const [key, value] of Object.entries(json)) {
      table +=
        `<tr>` +
        `<td style="width:30%">${key}</td>` +
        (typeof value === "string"
          ? `<td>${value}</td>`
          : `<td>${createElement(value)}</td>`) +
        `</tr>`;
    }
    divs += `<table break-words">${table}</table>`;
  }
  return divs;
}

const renderAdditional = (jsonString: string) => {
  try {
    const jsonList = JSON.parse(jsonString);
    return createElement(jsonList);
  } catch (e) {
    console.error(e);
    return null;
  }
};
</script>

<template>
  <UButton
    :label="!checkData.collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="checkData.collapse = !checkData.collapse"
  />
  <div v-if="checkData.collapse" class="border rounded p-3">
    <FormsCheckForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.checks.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.checks"
      :key="idx"
      class="border rounded p-3"
    >
      <FormsCheckForm
        v-if="checkData.edit && checkData.itemId == item['id'].toString()"
        :check="checkData.check"
        @cancel="cancelAction"
      />
      <div v-else>
        <p class="text-primary">
          {{ "Проверка кандидата #" + (idx + 1) }}
        </p>
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
        <ElementsLabelSlot :label="'Проверка в Крос'">
          {{ item["cros"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Комментарии'">{{
          item["comment"] ? item["comment"] : "-"
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Результат'">{{
          item["conclusion"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{
          item["username"]
        }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
        <ElementsLabelSlot v-if="item['addition']" :label="'Дополнительно'">
          <UButton
            label="Информация"
            variant="link"
            @click="checkData.collapseAdd = !checkData.collapseAdd"
          />
        </ElementsLabelSlot>
        <div
          v-if="item['addition'] && checkData.collapseAdd"
          class="border rounded p-3"
          v-html="renderAdditional(item['addition'])"
        />
        <ElementsNaviHorizontal
          v-show="
            !idx &&
            anketaState.anketa.value.persons['user_id'] ==
              userState.user.value.userId &&
            anketaState.anketa.value.persons['standing']
          "
          @update="
            checkData.check = item;
            checkData.itemId = item['id'].toString();
            checkData.edit = true;
          "
          @delete="anketaState.deleteItem(item['id'].toString(), 'checks')"
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
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Проверка кандидата отсутствует</p>
  </div>
</template>
