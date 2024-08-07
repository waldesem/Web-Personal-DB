<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Needs } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const actions = ref(false);
const edit = ref(false);
const itemId = ref("");
const need = ref(<Needs>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapseInquiry = document.getElementById("clps_inquiry");
  collapseInquiry?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <div class="collapse card card-body mb-3" id="clps_inquiry">
    <FormsInquiryForm @cancel="cancelAction" />
  </div>
  <div v-if="anketaState.anketa.value.inquiries.length">
    <div
      class="card card-body mb-3"
      v-for="(item, idx) in anketaState.anketa.value.inquiries"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
    >
      <FormsInquiryForm
        v-if="edit && itemId == item['id'].toString()"
        :inquiry="need"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
              actions && idx &&
              anketaState.anketa.value.persons['user_id'] == userState.user.value.userId &&
              anketaState.anketa.value.persons['standing']
            "
            @delete="anketaState.deleteItem(item['id'].toString(), 'inquiries')"
            @update="
              need = item;
              itemId = item['id'].toString();
              edit = true;
            "
            :hide="true"
          />
        </ElementsLabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Запросы о сотруднике #" + (idx + 1) }}
        </p>
        <ElementsLabelSlot :label="'Информация'">{{ item["info"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Иннициатор'">{{ item["origins"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{ item["username"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
      </div>
    </div>
  </div>
  <p class="p-3" v-else>Запросы о сотруднике не поступали</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>
