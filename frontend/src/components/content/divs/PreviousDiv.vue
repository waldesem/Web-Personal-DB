<script setup lang="ts">
import { defineAsyncComponent, reactive, ref } from "vue";
import { stateAnketa } from "@/state";
import { Previous } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const PreviousForm = defineAsyncComponent(
  () => import("@components/content/forms/PreviousForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const actions = ref(false);
const edit = ref(false);
const itemId = ref('');
const previous = reactive(<Previous>{});

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  const collapsePrevious = document.getElementById("previouser");
  collapsePrevious?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <DropDownHead :id="'previouser'" :header="'Изменение имени'" />
  <div class="collapse card card-body mb-3" id="previouser">
    <PreviousForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.previous.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.previous"
      :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false"
      class="card card-body mb-3"
    >
      <PreviousForm 
        v-if="edit && itemId == item['id'].toString()" 
        :previous="previous" 
        @cancel="cancelAction" 
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="actions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'previous')"
            @update="
              previous = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Фамилия'">
          {{ item["surname"] }}
        </LabelSlot>
        <LabelSlot :label="'Имя'">
          {{ item["firstname"] }}
        </LabelSlot>
        <LabelSlot v-if="item['patronymic']" :label="'Отчество'">
          {{ item["patronymic"] }}
        </LabelSlot>
        <LabelSlot v-if="item['changed']" :label="'Дата изменения'">
          {{ new Date(String(item["changed"])).toLocaleDateString("ru-RU") }}
        </LabelSlot>
        <LabelSlot v-if="item['reason']" :label="'Причина'">
          {{ item["reason"] }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>
