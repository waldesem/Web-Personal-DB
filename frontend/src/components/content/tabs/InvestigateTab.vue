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

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(() => {
  emit("get-item", "investigation");
});

const props = defineProps({
  printPage: {
    type: Boolean,
    default: false,
  },
});

const inquisition = ref({
  action: "",
  itemId: "",
  item: <Inquisition>{},
  showActions: false,
});

function submitForm(form: Object) {
  emit(
    "submit",
    inquisition.value.action,
    "investigation",
    inquisition.value.itemId,
    form
  );
  inquisition.value.action = "";
}
</script>

<template>
  <div class="py-3">
    <div class="text-end">
      <div class="text-end">
        <IconRelative v-if="inquisition.action !== 'create' && !props.printPage"
          :title="`Добавить`"
          :icon-class="`bi bi-incognito fs-1`"
          @onclick="inquisition.action = 'create'"
        />
      </div>
    </div>
    <InvestigationForm
      v-if="inquisition.action"
      :investigation="inquisition.item"
      @submit="submitForm"
      @cancel="inquisition.action = ''"
    />
    <div v-else
     @mouseover="inquisition.showActions = true"
     @mouseout="inquisition.showActions = false"
    >
      <div v-if="stateAnketa.investigation.length"> 
        <div class="mb-3" v-for="(item, idx) in stateAnketa.investigation" :key="idx">
          <div class="card card-body">
            <LabelSlot>
              <ActionIcons v-show="inquisition.showActions"
                @delete="emit('delete', item['id'].toString(), 'investigation')"
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
          </div>
        </div>
        <FileForm :accept="'*'" @submit="emit('file')" />
      </div>
      <p v-else>Данные отсутствуют</p>
    </div>
  </div>
</template>
