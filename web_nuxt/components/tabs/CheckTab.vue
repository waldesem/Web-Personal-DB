<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Verification } from "@/utils/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean;

const checkData = ref({
  collapse: false,
  collapseAdd: false,
  edit: false,
  itemId: "",
  check: {} as Verification,
});

const { refresh } = await useAsyncData("checks", async () => {
  await anketaState.getItem('checks');
});

async function updateCheck(checkForm: Verification) {
  closeAction();
  Promise.all([
    await anketaState.updateItem('checks', checkForm),
    await refresh(),
  ])
}

async function deleteCheck(index: string) {
  Promise.all([
    await anketaState.deleteItem(index, 'checks'),
    await refresh(),
  ])
}

async function cancelOperation() {
  await refresh();
  closeAction();
}

function closeAction() {
  checkData.value.edit = false;
  checkData.value.itemId = "";
  checkData.value.collapse = false;
}

function openFileForm(elementId: string) {
  document.getElementById(elementId)?.click();
}
</script>

<template>
  <UButton
    v-if="editState"
    class="py-3"
    :label="!checkData.collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="checkData.collapse = !checkData.collapse"
  />
  <Transition name="slide-fade">
    <div v-if="checkData.collapse" class="py-3">
      <UCard>
        <FormsCheckForm 
          @submit="updateCheck"
          @cancel="cancelOperation" 
        />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.checks.length">
    <div
      v-for="(item, index) in anketaState.anketa.value.checks"
      :key="index"
      class="py-1"
    >
      <UCard>
        <template #header>
          <div class="tex-base text-red-800 font-medium">
            {{ "Проверка кандидата ID #" + item["id"] }}
          </div>
        </template>
        <FormsCheckForm
          v-if="
            checkData.edit &&
            checkData.itemId ==
              anketaState.anketa.value.checks[index]['id'].toString()
          "
          :check="checkData.check"
          @cancel="cancelOperation"
          @submit="updateCheck"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Проверка по местам работы'">
            {{ anketaState.anketa.value.checks[index]["workplace"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка паспорта'">
            {{ anketaState.anketa.value.checks[index]["document"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка ИНН'">{{
            anketaState.anketa.value.checks[index]["inn"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка ФССП'">{{
            anketaState.anketa.value.checks[index]["debt"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка банкротства'">
            {{ anketaState.anketa.value.checks[index]["bankruptcy"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка БКИ'">{{
            anketaState.anketa.value.checks[index]["bki"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка судебных решений'">
            {{ anketaState.anketa.value.checks[index]["courts"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка аффилированности'">
            {{ anketaState.anketa.value.checks[index]["affilation"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка по списку террористов'">
            {{ anketaState.anketa.value.checks[index]["terrorist"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка в розыск'">{{
            anketaState.anketa.value.checks[index]["mvd"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка в открытых источниках'">
            {{ anketaState.anketa.value.checks[index]["internet"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Проверка в Кронос'">
            {{ anketaState.anketa.value.checks[index]["cronos"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дополнительная информация'">
            {{ anketaState.anketa.value.checks[index]["addition"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Комментарии'"
            >{{ anketaState.anketa.value.checks[index]["comment"] }}
          </ElementsLabelSlot>
          <ElementsLabelSlot :label="'Результат'">{{
            anketaState.anketa.value.checks[index]["conclusion"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Сотрудник'">{{
            anketaState.anketa.value.checks[index]["username"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Дата записи'">
            {{
              new Date(
                anketaState.anketa.value.checks[index]["created"] + " UTC"
              ).toLocaleString("ru-RU")
            }}
          </ElementsLabelSlot>
        </div>
        <template
          v-if="
            editState &&
            (!checkData.edit &&
            checkData.itemId !=
              anketaState.anketa.value.checks[index]['id'].toString())
          "
          #footer
        >
          <ElementsNaviHorizont
            v-show="!index && editState"
            @update="
              checkData.check = anketaState.anketa.value.checks[index];
              checkData.itemId =
                anketaState.anketa.value.checks[index]['id'].toString();
              checkData.edit = true;
            "
            @delete="deleteCheck(anketaState.anketa.value.checks[index]['id'])"
            @upload="openFileForm('check-file')"
          />
          <div v-show="false">
            <UInput
              id="check-file"
              type="file"
              accept="*"
              multiple
              @change="
                anketaState.submitFile(
                  $event,
                  'checks',
                  anketaState.share.value.candId
                )
              "
            />
          </div>
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Проверка кандидата отсутствует</p>
  </div>
</template>
