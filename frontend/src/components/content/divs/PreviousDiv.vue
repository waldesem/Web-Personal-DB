<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";
import { Previous } from "@/interfaces";

const ActionHeader = defineAsyncComponent(
  () => import("@components/content/elements/ActionHeader.vue")
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

onBeforeMount(async () => {
  await stateAnketa.getItem("previous");
});

const previous = ref({
  action: "",
  itemId: "",
  item: <Previous>{},
  showActions: false,
});

function cancelAction(){
  previous.value.action = "";
  previous.value.itemId = "";
  previous.value.item = <Previous>({});
};

function submitForm(form: Object) {
  stateAnketa.updateItem(
    "previous",
    form
  );
  cancelAction();
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
    @cancel="cancelAction"
  />
  <div
    v-if="stateAnketa.anketa.previous.length"
    class="collapse show"
    id="previous"
  >
    <div
      v-for="(item, idx) in stateAnketa.anketa.previous"
      :key="idx"
      @mouseover="previous.showActions = true"
      @mouseout="previous.showActions = false"
      class="card card-body mb-3"
    >
      <PreviousForm
        v-if="
          previous.action === 'update' &&
          previous.itemId === item['id'].toString()
        "
        :previous="previous.item"
        @submit="submitForm"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="previous.showActions"
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
        <LabelSlot v-if="item['patronymic']" :label="'Отчество'">
          {{ item["patronymic"] }}
        </LabelSlot>
        <LabelSlot v-if="item['changed']" :label="'Дата изменения'">
          {{
            new Date(String(item["changed"])).toLocaleDateString("ru-RU")
          }}
        </LabelSlot>
        <LabelSlot v-if="item['reason']" :label="'Причина'">
          {{ item["reason"] }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
