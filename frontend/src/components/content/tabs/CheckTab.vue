<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { stateAnketa, stateUser } from "@/state";
import { Verification } from "@/interfaces";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const CheckForm = defineAsyncComponent(
  () => import("@components/content/forms/CheckForm.vue")
);

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
  let elems = "";
  for (let json of jsonList) {
    let elem = "";
    for (const [key, value] of Object.entries(json)) {
      elem +=
        `<tr>` +
        `<td>${key}</td>` +
        (typeof value === "string"
          ? `<td>${value}</td>`
          : `<td>${createElement(value)}</td>`) +
        `</tr>`;
    }
    elems += elem;
  }
  return `<table class="table table-sm table-responsive table-striped">${elems}</table>`;
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
        <LabelSlot>
          <ActionIcons
            v-show="
              checkData.actions &&
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
          </ActionIcons>
        </LabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Проверка кандидата #" + (idx + 1) }}
        </p>
        <LabelSlot :label="'Проверка по местам работы'">
          {{ item["workplace"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка паспорта'">
          {{ item["document"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка ИНН'">{{ item["inn"] }}</LabelSlot>
        <LabelSlot :label="'Проверка ФССП'">{{ item["debt"] }}</LabelSlot>
        <LabelSlot :label="'Проверка банкротства'">
          {{ item["bankruptcy"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка БКИ'">{{ item["bki"] }}</LabelSlot>
        <LabelSlot :label="'Проверка судебных решений'">
          {{ item["courts"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка аффилированности'">
          {{ item["affilation"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка по списку террористов'">
          {{ item["terrorist"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка в розыск'">{{ item["mvd"] }}</LabelSlot>
        <LabelSlot :label="'Проверка в открытых источниках'">
          {{ item["internet"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка в Кронос'">
          {{ item["cronos"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка в Крос'">
          {{ item["cros"] }}
        </LabelSlot>
        <LabelSlot :label="'Комментарии'">{{
          item["comment"] ? item["comment"] : "-"
        }}</LabelSlot>
        <LabelSlot :label="'Результат'">{{ item["conclusion"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["username"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </LabelSlot>
        <LabelSlot
          class="d-print-none"
          :label="'Дополнительная информация'"
        >
          <button
            type="button"
            class="btn btn-link"
            data-bs-toggle="collapse"
            href="#clps_additional"
            role="button"
          >
            Показать
          </button>
        </LabelSlot>
        <div
          class="collapse card card-body mb-3"
          id="clps_additional"
        >
          <div
            v-if="item['addition']"
            v-html="renderAdditional(item['addition'])"
          ></div>
          <label
            v-else
            class="form-label text-primary text-decoration-underline"
            for="xml-file"
            style="cursor: pointer"
          >
            Загрузить XML
            <FileForm
              :accept="'.xml'"
              :name-id="'xml-file'"
              @submit="stateAnketa.submitFile($event, 'xml', item['id'])"
            />
          </label>
        </div>
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
