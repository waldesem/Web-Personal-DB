<script setup lang="ts">
import { ref } from "vue";
import { stateAnketa, stateUser } from "@/state/state";
import type { Staff } from "@/utils/interfaces";

const anketaState = stateAnketa();
const userState = stateUser();

const collapse = ref(false);
const edit = ref(false);
const itemId = ref("");
const staff = ref({} as Staff);

function cancelAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="p-1">
      <div class="border rounded p-3">
      <FormsStaffForm @cancel="cancelAction" />
      </div>
    </div>
  </Transition>
  <div v-if="anketaState.anketa.value.staffs.length">
    <div
      v-for="(item, idx) in anketaState.anketa.value.staffs"
      :key="idx"
      class="p-1"
    >
      <div class="border rounded pt-3 pb-1 px-3">
        <FormsStaffForm
          v-if="edit && itemId == item['id'].toString()"
          :staff="staff"
          @cancel="cancelAction"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Должность'">{{
            item["position"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Департамент'">{{
            item["department"]
          }}</ElementsLabelSlot>
          <ElementsNaviHorizontal
            v-show="
              anketaState.anketa.value.persons['user_id'] ==
                userState.user.value.userId &&
              anketaState.anketa.value.persons['editable']
            "
            :last-index="2"
            @delete="anketaState.deleteItem(item['id'].toString(), 'staffs')"
            @update="
              staff = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </div>
      </div>
    </div>
  </div>
  <div v-else class="p-3">
    <p class="text-primary">Данные о должностях отсутствуют</p>
  </div>
</template>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}
</style>