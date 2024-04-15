<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Needs } from "@/interfaces/interface";
import { classifyStore } from "@/store/classify";

const storeClassify = classifyStore();

const IconRelative = defineAsyncComponent(
  () => import("@components/content/elements/IconRelative.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const InquiryForm = defineAsyncComponent(
  () => import("@components/content/forms/InquiryForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item", "inquiry");
});

const props = defineProps({
  printPage: {
    type: Boolean,
    default: false,
  },
  needs: {
    type: Array as () => Array<Needs>,
    default: () => [],
  },
});

const need = ref({
  action: "",
  itemId: "",
  item: <Needs>{},
  showActions: false,
});

function submitForm(form: Object) {
  emit("submit", need.value.action, "inquiry", need.value.itemId, form);
  need.value.action = "";
};
</script>

<template>
  <div class="py-3">
    <div class="text-end">
      <IconRelative v-if="need.action !== 'create' && !props.printPage"
        :title="`Добавить`"
        :icon-class="`bi bi-question-square fs-1`"
        @onclick="need.action = 'create'"
      />
    </div>
    <InquiryForm v-if="need.action"
      :inquiry="need.item" 
      @submit="submitForm"
      @cancel="need.action = ''"
    />
    <div v-else
      @mouseover="need.showActions = true"
      @mouseout="need.showActions = false"
    >
      <div v-if="props.needs.length"> 
        <div class="mb-3" v-for="(item, idx) in props.needs" :key="idx">
          <div class="card card-body">
            <LabelSlot>
              <ActionIcons v-show="need.showActions"
                @delete="emit('delete', item['id'].toString(), 'inquiry')"
                @update="
                  need.action = 'update';
                  need.item = item;
                  need.itemId = item['id'].toString();
                "
              />
            </LabelSlot>
            <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
            <LabelSlot :label="'Иннициатор'">{{ item["initiator"] }}</LabelSlot>
            <LabelSlot :label="'Источник'">{{ item["source"] }}</LabelSlot>
            <LabelSlot :label="'Сотрудник'">{{ storeClassify.classData.users[item["user_id"]] }}</LabelSlot>
            <LabelSlot :label="'Дата запроса'">
              {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
            </LabelSlot>
          </div>
        </div>
      </div>
      <p v-else>Данные отсутствуют</p>
    </div>
  </div>
</template>
