<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Needs } from "@/interfaces";
import { stateAnketa, stateUser } from "@/state";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const InquiryForm = defineAsyncComponent(
  () => import("@components/content/forms/InquiryForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

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
    <InquiryForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.inquiries.length">
    <div
      class="card card-body mb-3"
      v-for="(item, idx) in stateAnketa.anketa.inquiries"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
    >
      <InquiryForm
        v-if="edit && itemId == item['id'].toString()"
        :inquiry="need"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="
              actions &&
              stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
              stateAnketa.anketa.persons['standing']
            "
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'inquiries')"
            @update="
              need = item;
              itemId = item['id'].toString();
              edit = true;
            "
            :hide="true"
          />
        </LabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Запросы о сотруднике #" + (idx + 1) }}
        </p>
        <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
        <LabelSlot :label="'Иннициатор'">{{ item["origins"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["username"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </LabelSlot>
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
