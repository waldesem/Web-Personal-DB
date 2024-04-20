<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { Previous } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
)
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const PreviousForm = defineAsyncComponent(
  () => import("@components/content/forms/PreviousForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit"]);

onBeforeMount(() => {
  emit("get-item");
});

const props = defineProps({
  printPage: {
    type: Boolean,
    default: false,
  },
  items: {
    type: Array<Previous>,
    default: [{}],
  },
});

const previous = ref({
  action: "",
  itemId: "",
  item: <Previous>{},
  showActions: false,
});

function submitForm(form: Object) {
  emit("submit", previous.value.action, "previous", previous.value.itemId, form);
  previous.value.action = "";
}
</script>

<template>
  <ActionHeader
    :print-page="props.printPage"
    :id="'previous'"
    :header="'Изменение имени'"
    :action="previous.action"
    @action="previous.action = previous.action ? '' : 'create'"
  />
  <PreviousForm 
    v-if="previous.action" 
    :previous="previous.item" 
    @submit="submitForm" 
    @cancel="previous.action = ''"
  />
  <div v-else
    @mouseover="previous.showActions = true"
    @mouseout="previous.showActions = false"
  >
    <div 
      v-if="props.items.length" 
      :class="{'collapse show': !printPage}" 
      id="previous"> 
      <div class="mb-3" v-for="(item, idx) in props.items" :key="idx">
        <div class="card card-body">
          <LabelSlot>
            <ActionIcons v-show="previous.showActions"
              @delete="emit('delete', item['id'].toString(), 'previous')"
              @update="
                previous.action = 'update';
                previous.item = item;
                previous.itemId = item['id'].toString();
              "
            />
          </LabelSlot>
          <LabelSlot :label="'Фамилия'">
            {{ item["surname"] }}
          </LabelSlot>
          <LabelSlot :label="'Имя'">
            {{ item["firstname"] }}
          </LabelSlot>
          <LabelSlot :label="'Отчество'">
            {{ item["patronymic"] }}
          </LabelSlot>
          <LabelSlot :label="'Дата изменения'">
            {{ new Date(String(item["date_change"])).toLocaleDateString(
            "ru-RU"
          ) }}
          </LabelSlot>
          <LabelSlot :label="'Причина'">
            {{ item["reason"] }}
          </LabelSlot>
        </div>
      </div>
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
