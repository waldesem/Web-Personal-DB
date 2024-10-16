<script setup lang="ts">
import type { Staff } from "@/types/interfaces";

prefetchComponents(["FormsStaffForm", "ElementsSkeletonDiv"]);

const emit = defineEmits(["delete", "submit"]);

const authFetch = useFetchAuth();

const props = defineProps({
  candId: {
    type: String,
    default: "",
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

const collapse = ref(false);
const pending = ref(false);
const edit = ref(false);
const itemId = ref("");
const staff = ref({} as Staff);
const staffs = ref<Staff[]>([]);

const { refresh, status } = await useLazyAsyncData("staffs", async () => {
  staffs.value = await authFetch("/api/items/staffs/" + props.candId) as Staff[];
});

async function submitStaff(form: Staff) {
  closeAction();  
  pending.value = true;
  await emit("submit", form, "staffs");
  pending.value = false;
  await refresh();
}

async function deleteStaff(id: string) {
  closeAction();
  await emit("delete", id, "staffs");
  await refresh();
}

function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  edit.value = false;
  itemId.value = "";
  collapse.value = false;
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :label="!collapse ? 'Добавить запись' : 'Скрыть форму'"
    variant="link"
    @click="collapse = !collapse"
  />
  <Transition name="slide-fade">
    <div v-if="collapse" class="py-3">
      <ElementsCardDiv>
        <FormsStaffForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitStaff"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="staffs && staffs.length">
    <div v-for="(item, idx) in staffs" :key="idx" class="p-1">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="2" />
      <ElementsCardDiv v-else>
        <FormsStaffForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :staff="staff"
          @cancel="cancelOperation"
          @update="submitStaff"
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
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deleteStaff(item['id'])"
            @update="
              staff = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="2" />
    <p v-else class="text-primary">Данные о должностях отсутствуют</p>
  </div>
</template>
