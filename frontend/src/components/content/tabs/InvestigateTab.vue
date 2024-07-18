<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces";
import { stateAnketa, stateUser } from "@/state";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const InvestigationForm = defineAsyncComponent(
  () => import("@components/content/forms/InvestigationForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const actions = ref(false);
const edit = ref(false);
const itemId = ref("");
const inquisition = ref(<Inquisition>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapseInvestigation = document.getElementById("clps_investigate");
  collapseInvestigation?.setAttribute("class", "collapse card card-body");
}
</script>

<template>
  <div class="collapse card card-body mb-3" id="clps_investigate">
    <InvestigationForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.investigations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.investigations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <InvestigationForm
        v-if="edit && itemId == item['id'].toString()"
        :investigation="inquisition"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="
              actions &&
              stateAnketa.anketa.persons['user_id'] == stateUser.userId &&
              stateAnketa.anketa.persons['standing']
            "
            @delete="
              stateAnketa.deleteItem(item['id'].toString(), 'investigations')
            "
            @update="
              inquisition = item;
              itemId = item['id'].toString();
              edit = true;
            "
            :for-input="'investigations-file'"
          >
            <FileForm
              v-show="actions"
              :name-id="'investigations-file'"
              :accept="'*'"
              @submit="
                stateAnketa.submitFile(
                  $event,
                  'investigations',
                  stateAnketa.share.candId
                )
              "
            />
          </ActionIcons>
        </LabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Расследование/Проверка #" + (idx + 1) }}
        </p>
        <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
        <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["username"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p class="p-3" v-else>Расследования/Проверки не проводились</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>
