<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "../../utils/state";
import type { Verification } from "../../utils/interfaces";

const checkData = ref({
  actions: false,
  edit: false,
  itemId: "",
  check: <Verification>{},
});

function cancelAction() {
  checkData.value.edit = false;
  checkData.value.itemId = "";
  const collapseCheck = document.getElementById("clps_check");
  collapseCheck?.setAttribute("class", "collapse card card-body mb-3");
}

function createElement(jsonList: Array<Object>) {
  let divs = "";
  for (let json of jsonList) {
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
    divs += `<table class="table table-sm table-striped text-break">${table}</table>`;
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
  <div class="collapse card card-body mb-3" id="clps_check">
    <CheckForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.checks.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.checks"
      class="card card-body mb-3"
      :key="idx"
      @mouseover="checkData.actions = true"
      @mouseout="checkData.actions = false"
    >
      <CheckForm
        v-if="checkData.edit && checkData.itemId == item['id'].toString()"
        :check="checkData.check"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
              checkData.actions && !idx &&
              stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
              stateAnketa.anketa.persons['standing']
            "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'checks')"
            @update="
              checkData.check = item;
              checkData.itemId = item['id'].toString();
              checkData.edit = true;
            "
            :for-input="'check-file'"
          >
            <FileForm
              v-show="checkData.actions"
              :name-id="'check-file'"
              :accept="'*'"
              @submit="
                stateAnketa.submitFile(
                  $event,
                  'checks',
                  stateAnketa.share.candId
                )
              "
            />
          </ElementsActionIcons>
        </ElementsLabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Проверка кандидата #" + (idx + 1) }}
        </p>
        <ElementsLabelSlot :label="'Проверка по местам работы'">
          {{ item["workplace"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка паспорта'">
          {{ item["document"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка ИНН'">{{ item["inn"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка ФССП'">{{ item["debt"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка банкротства'">
          {{ item["bankruptcy"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка БКИ'">{{ item["bki"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка судебных решений'">
          {{ item["courts"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка аффилированности'">
          {{ item["affilation"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка по списку террористов'">
          {{ item["terrorist"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Проверка в розыск'">{{ item["mvd"] }}</ElementsLabelSlot>
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
        <ElementsLabelSlot :label="'Результат'">{{ item["conclusion"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{ item["username"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="item['addition']"
          class="d-print-none"
          :label="'Дополнительно'"
        >
          <button
            type="button"
            class="btn btn-link"
            data-bs-toggle="collapse"
            href="#clps_additional"
            role="button"
          >
            Информация
          </button>
        </ElementsLabelSlot>
        <div
          class="collapse card card-body"
          id="clps_additional"
          v-if="item['addition']"
          v-html="renderAdditional(item['addition'])"
        ></div>
      </div>
    </div>
  </div>
  <p class="p-3" v-else>Проверка кандидата отсутствует</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>
