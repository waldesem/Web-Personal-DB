<script setup lang="ts">
import { ref, defineAsyncComponent, computed } from "vue";
import { classifyStore } from "@store/classify";
import { Verification } from "@/interfaces/interface";

const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectInput = defineAsyncComponent(
  () => import("@components/content/elements/SelectInput.vue")
);
const SwitchBox = defineAsyncComponent(
  () => import("@components/content/elements/SwitchBox.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const storeClassify = classifyStore();

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  check: {
    type: Object as () => Verification,
    default: {},
  },
});

const checkForm = computed(() => {
  return props.check as Verification;
});

const noNegative = ref(true);

computed(() => {
  if (noNegative) {
    Object.assign(checkForm.value, {
      workplace: "Негатива по местам работы не обнаружено",
      employee: "В числе бывших работников МТСБ не обнаружен",
      document: "Среди недействительных документов не обнаружен",
      inn: "ИНН соответствует паспорту",
      debt: "Задолженности не обнаружены",
      bankruptcy: "Решений о признании банкротом не имеется",
      bki: "Кредитная история не положительная",
      courts: "Судебные дела не обнаружены",
      affiliation: "Аффилированность не выявлена",
      terrorist: "В списке террористов не обнаружен",
      mvd: "В розыск не объявлен",
      internet: "В открытых источниках негатив не обнаружен",
      cronos: "В Кронос негатив не выявлен",
      cros: "В Крос негатив не выявлен",
      addition: "Дополнительная информация отсутствует",
    });
  } else {
    Object.keys(checkForm.value).forEach((key) => {
      delete checkForm.value[key as keyof typeof checkForm.value];
    });
  };
})
</script>

<template>
  <SwitchBox
    :name="'noNegative'"
    :place="'Негатива нет'"
    v-model="noNegative"
  />
  <form
    @submit.prevent="emit('submit', checkForm)"
    class="form form-check"
    role="form"
    id="checkFormId"
  >
    <LabelSlot :label="'Проверка по местам работы'">
      <TextArea
        :name="'workplace'"
        :place="'Проверка по местам работы'"
        v-model="props.check['workplace']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка по кадровому учету'">
      <TextArea
        :name="'employee'"
        :place="'Проверка по кадровому учету'"
        v-model="props.check['employee']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка документов'">
      <TextArea
        :name="'document'"
        :place="'Проверка документов'"
        v-model="props.check['document']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка ИНН'">
      <TextArea
        :name="'inn'"
        :place="'Проверка ИНН'"
        v-model="props.check['inn']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка задолженностей'">
      <TextArea
        :name="'debt'"
        :place="'Проверка задолженностей'"
        v-model="props.check['debt']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка решений о признании банкротом'">
      <TextArea
        :name="'bankruptcy'"
        :place="'Проверка решений о признании банкротом'"
        v-model="props.check['bankruptcy']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка кредитной истории'">
      <TextArea
        :name="'bki'"
        :place="'Проверка кредитной истории'"
        v-model="props.check['bki']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка судебных дел'">
      <TextArea
        :name="'courts'"
        :place="'Проверка судебных дел'"
        v-model="props.check['courts']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка аффилированности'">
      <TextArea
        :name="'affiliation'"
        :place="'Проверка аффилированности'"
        v-model="props.check['affiliation']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка в списке террористов'">
      <TextArea
        :name="'terrorist'"
        :place="'Проверка в списке террористов'"
        v-model="props.check['terrorist']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка в розыск'">
      <TextArea
        :name="'mvd'"
        :place="'Проверка в розыск'"
        v-model="props.check['mvd']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка в открытых источниках'">
      <TextArea
        :name="'internet'"
        :place="'Проверка в открытых источниках'"
        v-model="props.check['internet']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка в Кронос'">
      <TextArea
        :name="'cronos'"
        :place="'Проверка в Кронос'"
        v-model="props.check['cronos']"
      />
    </LabelSlot>
    <LabelSlot :label="'Проверка в Крос'">
      <TextArea
        :name="'cros'"
        :place="'Проверка в Крос'"
        v-model="props.check['cros']"
      />
    </LabelSlot>
    <LabelSlot :label="'Дополнительная информация'">
      <TextArea
        :name="'addition'"
        :place="'Дополнительная информация'"
        v-model="props.check['addition']"
      />
    </LabelSlot>
    <SwitchBox
      :div-class="'offset-lg-2 col-lg-10'"
      :name="'pfo'"
      :place="'Полиграф'"
      v-model="checkForm['pfo']"
    />
    <LabelSlot :label="'Результат'">
      <SelectInput
        :name="'conclusion'"
        :select="storeClassify.classData.conclusion"
        v-model="checkForm['conclusion']"
      />
    </LabelSlot>
    <LabelSlot :label="'Комментарий'">
      <TextArea
        :name="'comments'"
        :place="'Комментарий'"
        v-model="props.check['comments']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"  
      />
    </BtnGroup>
  </form>
</template>
