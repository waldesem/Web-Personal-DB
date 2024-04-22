<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Inquisition } from "@/interfaces";
import { stateClassify, stateAnketa } from "@/state";

const IconRelative = defineAsyncComponent(
  () => import("@components/content/elements/IconRelative.vue")
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

onBeforeMount(async() => {
  await stateAnketa.getItem("investigation");
});

const inquisition = ref({
  action: "",
  itemId: "",
  item: <Inquisition>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(
    inquisition.value.action,
    "investigation",
    inquisition.value.itemId,
    form
  );
  inquisition.value.action = "";
  inquisition.value.itemId = "";
}
</script>

<template>
  <IconRelative v-show="inquisition.action !== 'create' && !stateAnketa.share.printPage"
    :title="`Добавить`"
    :icon-class="`bi bi-incognito fs-1`"
    @onclick="inquisition.action = 'create'"
  />
  <InvestigationForm
    v-if="inquisition.action === 'create'"
    @submit="submitForm"
    @cancel="inquisition.action = ''; inquisition.itemId = ''"
  />
  <div v-if="stateAnketa.anketa.investigation.length"> 
    <div 
      v-for="(item, idx) in stateAnketa.anketa.investigation" :key="idx"
      class="mb-3"
      :class="{ 'card card-body': !stateAnketa.share.printPage }"
      @mouseover="inquisition.showActions = true"
      @mouseout="inquisition.showActions = false"
    >
      <LabelSlot>
        <ActionIcons v-show="inquisition.showActions"
          @delete="stateAnketa.deleteItem(item['id'].toString(), 'investigation')"
          @update="
            inquisition.action = 'update';
            inquisition.item = item;
            inquisition.itemId = item['id'].toString();
          "
        />
      </LabelSlot>
      <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
      <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
      <LabelSlot :label="'Сотрудник'">{{ stateClassify.users[item["user_id"]] }}</LabelSlot>
      <LabelSlot :label="'Дата'">
        {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
      </LabelSlot>
      <FileForm :accept="'*'" @submit="stateAnketa.submitFile($event, 'investigation')" />
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
