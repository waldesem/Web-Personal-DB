<script setup lang="ts">
import { ref, defineAsyncComponent, computed } from "vue";
import { classifyStore } from "@store/classify";
import { Verification } from "@/interfaces/interface";

const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
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
};
</script>

<template>
  <div class="form-check form-switch">
    <input
      class="form-check-checkbox"
      role="switch"
      id="checkbox"
      name="check"
      type="checkbox"
      v-model="noNegative"
    />
    <label class="form-check-label" for="checkbox">Негатива нет</label>
  </div>

  <form
    @submit.prevent="emit('submit', checkForm)"
    class="form form-check"
    role="form"
    id="checkFormId"
  >
    <TextLabel
      :name="'workplace'"
      :label="'Проверка по местам работы'"
      v-model="props.check['workplace']"
    />
    <TextLabel
      :name="'employee'"
      :label="'Проверка по кадровому учету'"
      v-model="props.check['employee']"
    />
    <TextLabel
      :name="'document'"
      :label="'Проверка документов'"
      v-model="props.check['document']"
    />
    <TextLabel
      :name="'inn'"
      :label="'Проверка ИНН'"
      v-model="props.check['inn']"
    />
    <TextLabel
      :name="'debt'"
      :label="'Проверка задолженностей'"
      v-model="props.check['debt']"
    />
    <TextLabel
      :name="'bankruptcy'"
      :label="'Проверка решений о признании банкротом'"
      v-model="props.check['bankruptcy']"
    />
    <TextLabel
      :name="'bki'"
      :label="'Проверка кредитной истории'"
      v-model="props.check['bki']"
    />
    <TextLabel
      :name="'courts'"
      :label="'Проверка судебных дел'"
      v-model="props.check['courts']"
    />
    <TextLabel
      :name="'affiliation'"
      :label="'Проверка аффилированности'"
      v-model="props.check['affiliation']"
    />
    <TextLabel
      :name="'terrorist'"
      :label="'Проверка в списке террористов'"
      v-model="props.check['terrorist']"
    />
    <TextLabel
      :name="'mvd'"
      :label="'Проверка в розыск'"
      v-model="props.check['mvd']"
    />
    <TextLabel
      :name="'internet'"
      :label="'Проверка в открытых источниках'"
      v-model="props.check['internet']"
    />
    <TextLabel
      :name="'cronos'"
      :label="'Проверка в Кронос'"
      v-model="props.check['cronos']"
    />
    <TextLabel
      :name="'cros'"
      :label="'Проверка в Крос'"
      v-model="props.check['cros']"
    />
    <TextLabel
      :name="'addition'"
      :label="'Дополнительная информация'"
      v-model="props.check['addition']"
    />
    <div class="row">
      <div class="offset-lg-2 col-lg-10">
        <div class="mb-3 form-check">
          <input
            class="form-check-input"
            id="pfo"
            name="pfo"
            v-model="checkForm['pfo']"
            type="checkbox"
            value="y"
          />
          <label class="form-check-label" for="pfo">Полиграф</label>
        </div>
      </div>
    </div>
    <SelectDiv
      :name="'conclusion'"
      :label="'Результат'"
      :select="storeClassify.classData.conclusion"
      v-model="checkForm['conclusion']"
    />
    <TextLabel
      :name="'comments'"
      :label="'Комментарий'"
      v-model="props.check['comments']"
    />
    <BtnGroup>
      <button
        class="btn btn-outline-primary btn-md"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      <button 
        class="btn btn-outline-secondary btn-md" 
        name="reset" 
        type="reset"
      >
        Очистить
      </button>
      <button
        class="btn btn-outline-danger btn-md"
        type="button"
        @click="emit('cancel')"
        name="cancel"
      >
      Отмена
      </button>
    </BtnGroup>
  </form>
</template>
