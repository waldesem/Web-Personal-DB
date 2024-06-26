<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces";
import { stateAnketa, submitFile } from "@/state";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
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

const inquisition = ref({
  itemId: "",
  item: <Inquisition>{},
  showActions: false,
});

function cancelAction() {
  inquisition.value.itemId = "";
  Object.keys(inquisition.value.item).forEach(
    (key) =>
      delete inquisition.value.item[key as keyof typeof inquisition.value.item]
  );
  const collapseInvestigation = document.getElementById("investigation");
  collapseInvestigation?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <DropDownHead
    :id="'investigation'"
    :header="'Расследования и служебные проверки:'"
  />
  <div class="collapse card card-body mb-3" id="investigation">
    <InvestigationForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.investigations.length" class="py-3">
    <div
      v-for="(item, idx) in stateAnketa.anketa.investigations"
      :key="idx"
      @mouseover="inquisition.showActions = true"
      @mouseout="inquisition.showActions = false"
      class="card card-body mb-3"
    >
      <InvestigationForm
        v-if="inquisition.itemId === item['id'].toString()"
        :investigation="inquisition.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="inquisition.showActions"
            @delete="
              stateAnketa.deleteItem(item['id'].toString(), 'investigations')
            "
            @update="
              inquisition.item = item;
              inquisition.itemId = item['id'].toString();
            "
            :for-input="'investigations-file'"
          >
            <FileForm
              v-show="inquisition.showActions"
              :name-id="'investigations-file'"
              :accept="'*'"
              @submit="submitFile($event, 'investigations')"
            />
          </ActionIcons>
        </LabelSlot>
        <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
        <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"]).toLocaleString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p class="px-3" v-else>Не проводились</p>
</template>
