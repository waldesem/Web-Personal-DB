<script setup lang="ts">
import { stateAnketa } from "@/state/state";
import type { Staff } from "@/utils/interfaces";

const anketaState = stateAnketa();

const editState = inject("editState") as boolean

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const staff = ref({} as Staff);

const { refresh } = await useAsyncData("staffs", async () => {
  await anketaState.getItem('staffs');
})

async function updateStaff(staffForm: Staff) {
  await anketaState.updateItem("staffs", staffForm);
  await refresh();
}

async function deleteStaff(index: string) {
  await anketaState.deleteItem(index, 'staffs');
  await refresh();
}

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="editState"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <UCard>
        <FormsStaffForm 
          @cancel="cancelAction" 
          @submit="updateStaff"
        />
      </UCard>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.staffs.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.staffs"
      :key="idx"
      class="p-1"
    >
      <UCard>
        <FormsStaffForm
          v-if="edit && itemId == item['id'].toString()"
          :staff="staff"
          @cancel="cancelAction"
          @submit="updateStaff"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Должность'">{{
            item["position"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Департамент'">{{
            item["department"]
          }}</ElementsLabelSlot>
        </div>
        <template
          v-if="editState && (!edit || itemId != item['id'].toString())"
          #footer
        >
        <ElementsNaviHorizont
            v-show="editState"
            :last-index="2"
            @delete="deleteStaff(item['id'])"
            @update="
              staff = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные о должностях отсутствуют</p>
  </div>
</template>

