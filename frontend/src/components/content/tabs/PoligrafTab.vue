<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Pfo } from "@/interfaces";
import { stateClassify, stateAnketa } from "@/state";

const IconRelative = defineAsyncComponent(
  () => import("@components/content/elements/IconRelative.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const PoligrafForm = defineAsyncComponent(
  () => import("@components/content/forms/PoligrafForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(async() => {
  await stateAnketa.getItem("poligraf");
});

const poligraf = ref({
  action: "",
  itemId: "",
  item: <Pfo>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(
    poligraf.value.action,
    "poligraf",
    poligraf.value.itemId,
    form
  );
  Object.keys(form).forEach((key) => {
    delete form[key as keyof typeof form];
  });
  poligraf.value.action = "";
  poligraf.value.itemId = "";
}
</script>

<template>
  <IconRelative 
    v-show="poligraf.action !== 'create'"
    :title="`Добавить`"
    :icon-class="`bi bi-heart-pulse fs-1`"
    @onclick="poligraf.action = 'create'"
  />
  <PoligrafForm
    v-if="poligraf.action === 'create'"
    @submit="submitForm"
    @cancel="poligraf.action = ''; poligraf.itemId = ''"
  />
  <div v-if="stateAnketa.anketa.poligraf.length"> 
    <div
      class="mb-3"
      :class="{'collapse show': !stateAnketa.share.printPage}"
      v-for="(item, idx) in stateAnketa.anketa.poligraf" :key="idx"
      @mouseover="poligraf.showActions = true"
      @mouseout="poligraf.showActions = false"
    >
      <LabelSlot>
        <ActionIcons v-show="poligraf.showActions"
          :show-form="true"
          @delete="stateAnketa.deleteItem(item['id'].toString(), 'poligraf')"
          @update="
            poligraf.action = 'update';
            poligraf.item = item;
            poligraf.itemId = item['id'].toString();
          "
        >
        <FileForm 
          v-show="poligraf.showActions" 
          :accept="'*'" 
          @submit="stateAnketa.submitFile($event, 'poligraf')" 
        />
      </ActionIcons>
      </LabelSlot>
      <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
      <LabelSlot :label="'Результат'">{{ item["results"] }}</LabelSlot>
      <LabelSlot :label="'Сотрудник'">{{ stateClassify.users[item["user_id"]] }}</LabelSlot>
      <LabelSlot :label="'Дата'">
        {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
      </LabelSlot>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
