<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
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

const emit = defineEmits(["submit"]);

const props = defineProps({
  check: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const checkForm = ref({
  form: <Verification>{},
  noNegative: true,

  updateItem: function () {
    emit("submit", this.form);
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
   },
});


if (checkForm.value.noNegative) {
  Object.assign(checkForm.value.form, {
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
      v-model="checkForm.noNegative"
    />
    <label class="form-check-label" for="checkbox">Негатива нет</label>
  </div>

  <form
    @submit.prevent="checkForm.updateItem"
    class="form form-check"
    role="form"
    id="checkFormId"
  >
    <TextLabel
      :name="'workplace'"
      :label="'Проверка по местам работы'"
      :model="props.check['workplace']"
      @input-event="
        checkForm.form['workplace'] = $event.target.value
      "
    />
    <TextLabel
      :name="'employee'"
      :label="'Проверка по кадровому учету'"
      :model="props.check['employee']"
      @input-event="
        checkForm.form['employee'] = $event.target.value
      "
    />
    <TextLabel
      :name="'document'"
      :label="'Проверка документов'"
      :model="props.check['document']"
      @input-event="
        checkForm.form['document'] = $event.target.value
      "
    />
    <TextLabel
      :name="'inn'"
      :label="'Проверка ИНН'"
      :model="props.check['inn']"
      @input-event="checkForm.form['inn'] = $event.target.value"
    />
    <TextLabel
      :name="'debt'"
      :label="'Проверка задолженностей'"
      :model="props.check['debt']"
      @input-event="checkForm.form['debt'] = $event.target.value"
    />
    <TextLabel
      :name="'bankruptcy'"
      :label="'Проверка решений о признании банкротом'"
      :model="props.check['bankruptcy']"
      @input-event="
        checkForm.form['bankruptcy'] = $event.target.value
      "
    />
    <TextLabel
      :name="'bki'"
      :label="'Проверка кредитной истории'"
      :model="props.check['bki']"
      @input-event="checkForm.form['bki'] = $event.target.value"
    />
    <TextLabel
      :name="'courts'"
      :label="'Проверка судебных дел'"
      :model="props.check['courts']"
      @input-event="
        checkForm.form['courts'] = $event.target.value
      "
    />
    <TextLabel
      :name="'affiliation'"
      :label="'Проверка аффилированности'"
      :model="props.check['affiliation']"
      @input-event="
        checkForm.form['affiliation'] = $event.target.value
      "
    />
    <TextLabel
      :name="'terrorist'"
      :label="'Проверка в списке террористов'"
      :model="props.check['terrorist']"
      @input-event="
        checkForm.form['terrorist'] = $event.target.value
      "
    />
    <TextLabel
      :name="'mvd'"
      :label="'Проверка в розыск'"
      :model="props.check['mvd']"
      @input-event="checkForm.form['mvd'] = $event.target.value"
    />
    <TextLabel
      :name="'internet'"
      :label="'Проверка в открытых источниках'"
      :model="props.check['internet']"
      @input-event="
        checkForm.form['internet'] = $event.target.value
      "
    />
    <TextLabel
      :name="'cronos'"
      :label="'Проверка в Кронос'"
      :model="props.check['cronos']"
      @input-event="
        checkForm.form['cronos'] = $event.target.value
      "
    />
    <TextLabel
      :name="'cros'"
      :label="'Проверка в Крос'"
      :model="props.check['cros']"
      @input-event="checkForm.form['cros'] = $event.target.value"
    />
    <TextLabel
      :name="'addition'"
      :label="'Дополнительная информация'"
      :model="props.check['addition']"
      @input-event="
        checkForm.form['addition'] = $event.target.value
      "
    />
    <div class="row">
      <div class="offset-lg-2 col-lg-10">
        <div class="mb-3 form-check">
          <input
            class="form-check-input"
            id="pfo"
            name="pfo"
            v-model="props.check['pfo']"
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
      :model="props.check['conclusion']"
      @input-event="
        checkForm.form['conclusion'] = $event.target.value
      "
    />
    <TextLabel
      :name="'comments'"
      :label="'Комментарий'"
      :model="props.check['comments']"
      @input-event="
        checkForm.form['comments'] = $event.target.value
      "
    />
    <BtnGroup :cls="false">
      <button
        class="btn btn-outline-success btn-md"
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
    </BtnGroup>
  </form>
</template>
