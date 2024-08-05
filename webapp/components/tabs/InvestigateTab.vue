<script setup lang="ts">
import { ref } from "vue";
import type { Inquisition } from "@/utils/interfaces";
import { stateAnketa, stateUser } from "@/utils/state";

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
    <FormsInvestigationForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.investigations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.investigations"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <FormsInvestigationForm
        v-if="edit && itemId == item['id'].toString()"
        :investigation="inquisition"
        @cancel="cancelAction"
      />
      <div v-else>
        <ElementsLabelSlot>
          <ElementsActionIcons
            v-show="
              actions && idx &&
              stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
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
            <FormsFileForm
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
          </ElementsActionIcons>
        </ElementsLabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Расследование/Проверка #" + (idx + 1) }}
        </p>
        <ElementsLabelSlot :label="'Тема проверки'">{{ item["theme"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Информация'">{{ item["info"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Сотрудник'">{{ item["username"] }}</ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + " UTC").toLocaleString("ru-RU") }}
        </ElementsLabelSlot>
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
