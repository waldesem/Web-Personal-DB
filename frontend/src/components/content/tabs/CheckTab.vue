<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { stateAnketa, submitFile } from "@/state";
import { Verification } from "@/interfaces";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const CheckForm = defineAsyncComponent(
  () => import("@components/content/forms/CheckForm.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  tabAction: {
    type: String,
    default: "",
  },
  currentTab: {
    type: String,
    default: "",
  },
});

const check = ref({
  itemId: "",
  item: <Verification>{},
  showActions: false,
});

function cancelAction() {
  check.value.itemId = "";
  Object.keys(check.value.item).forEach(
    (key) => delete check.value.item[key as keyof typeof check.value.item]
  );
  emit("cancel");
}
</script>

<template>
  <CheckForm
    v-if="props.tabAction === 'create' && props.currentTab === 'CheckTab'"
    @cancel="cancelAction"
  />
  <div v-if="stateAnketa.anketa.checks.length" class="py-3">
    <div
      v-for="(item, idx) in stateAnketa.anketa.checks"
      :key="idx"
      @mouseover="check.showActions = true"
      @mouseout="check.showActions = false"
      class="card card-body mb-3"
    >
      <CheckForm
        v-if="check.itemId === item['id'].toString()"
        :check="check.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="check.showActions"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'checks')"
            @update="
              check.item = item;
              check.itemId = item['id'].toString();
            "
            :for-input="'check-file'"
          >
            <FileForm
              v-show="check.showActions"
              :name-id="'check-file'"
              :accept="'*'"
              @submit="submitFile($event, 'checks')"
            />
          </ActionIcons>
        </LabelSlot>
        <LabelSlot :label="'Проверка по местам работы'">
          {{ item["workplace"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка паспорта'">
          {{ item["document"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка ИНН'">{{ item["inn"] }}</LabelSlot>
        <LabelSlot :label="'Проверка ФССП'">{{ item["debt"] }}</LabelSlot>
        <LabelSlot :label="'Проверка банкротства'">
          {{ item["bankruptcy"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка БКИ'">{{ item["bki"] }}</LabelSlot>
        <LabelSlot :label="'Проверка судебных решений'">
          {{ item["courts"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка аффилированности'">
          {{ item["affilation"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка по списку террористов'">
          {{ item["terrorist"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка в розыск'">{{ item["mvd"] }}</LabelSlot>
        <LabelSlot :label="'Проверка в открытых источниках'">
          {{ item["internet"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка в Кронос'">
          {{ item["cronos"] }}
        </LabelSlot>
        <LabelSlot :label="'Проверка в Крос'">
          {{ item["cros"] }}
        </LabelSlot>
        <LabelSlot :label="'Дополнительная информация'">
          {{ item["addition"] }}
        </LabelSlot>
        <LabelSlot :label="'ПФО'">{{ item["pfo"] ? "Да" : "Нет" }}</LabelSlot>
        <LabelSlot :label="'Комментарии'">{{
          item["comment"] ? item["comment"] : "-"
        }}</LabelSlot>
        <LabelSlot :label="'Результат'">{{ item["conclusion"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"]).toLocaleString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>
