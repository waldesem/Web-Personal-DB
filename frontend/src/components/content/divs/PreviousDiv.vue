<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
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

onBeforeMount(async () => {
  await stateAnketa.getItem("previous");
});

const previous = ref({
  action: "",
  itemId: "",
  item: <Previous>{},
  showActions: false,
});

function submitForm(form: Object) {
  stateAnketa.updateItem(previous.value.action, "previous", previous.value.itemId, form);
  previous.value.action = "";
  previous.value.itemId = "";
}
</script>

<template>
  <ActionHeader
    :id="'previous'"
    :header="'Изменение имени'"
    :action="previous.action"
    @action="previous.action = previous.action ? '' : 'create'"
  />
  <PreviousForm 
    v-if="previous.action === 'create'" 
    :previous="previous.item" 
    @submit="submitForm" 
    @cancel="previous.action = ''; previous.itemId = ''"
  />
  <div v-else
    @mouseover="previous.showActions = true"
    @mouseout="previous.showActions = false"
  >
    <div 
      v-if="stateAnketa.anketa.previous.length" 
      :class="{'collapse show': !stateAnketa.share.printPage}" 
      id="previous"> 
      <div class="mb-3" v-for="(item, idx) in stateAnketa.anketa.previous" :key="idx">
        <div :class="{ 'card card-body': !stateAnketa.share.printPage }">
          <PreviousForm
            v-if="
              previous.action === 'update' &&
              previous.itemId === item['id'].toString()
            "
            :previous="previous.item"
            @submit="submitForm"
            @cancel="
              previous.action = '';
              previous.itemId = '';
            "
          />
          <div v-else>
            <LabelSlot>
              <ActionIcons v-show="previous.showActions"
                @delete="stateAnketa.deleteItem(item['id'].toString(), 'previous')"
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
    </div>
    <p v-else>Данные отсутствуют</p>
  </div>
</template>
