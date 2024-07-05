<script setup lang="ts">
import { ref, reactive, defineAsyncComponent } from "vue";
import { stateAnketa, stateUser, submitFile } from "@/state";
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

const actions = ref(false);
const edit = ref(false);
const itemId = ref("");
const check = reactive(<Verification>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapseCheck = document.getElementById("clps_check");
  collapseCheck?.setAttribute("class", "collapse card card-body mb-3");
}
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
      @mouseover="actions = true"
      @mouseout="actions = false"
    >
      <CheckForm
        v-if="edit && itemId == item['id'].toString()"
        :check="check"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="
              actions &&
              stateAnketa.anketa.persons['user_id'] == stateUser.userId
            "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'checks')"
            @update="
              check = item;
              itemId = item['id'].toString();
              edit = true;
            "
            :for-input="'check-file'"
          >
            <FileForm
              v-show="actions"
              :name-id="'check-file'"
              :accept="'*'"
              @submit="submitFile($event, 'checks')"
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
        <LabelSlot :label="'Дополнительная информация'">
          {{ item["addition"] }}
        </LabelSlot>
        <LabelSlot :label="'ПФО'">{{ item["pfo"] ? "Да" : "Нет" }}</LabelSlot>
        <LabelSlot :label="'Комментарии'">{{
          item["comment"] ? item["comment"] : "-"
        }}</LabelSlot>
        <LabelSlot :label="'Результат'">{{ item["conclusion"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </LabelSlot>
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
