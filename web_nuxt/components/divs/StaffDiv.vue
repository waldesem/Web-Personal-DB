<script setup lang="ts">
import type { Staff } from "@/types";

const emit = defineEmits(["message"]);

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

const modal = ref(false);
const pending = ref(false);
const staff = ref({} as Staff);
const staffs = ref<Staff[]>([]);

const { refresh, status } = await useLazyAsyncData("staffs", async () => {
  staffs.value = (await authFetch(
    "/route/items/staffs/" + props.candId
  )) as Staff[];
});

async function submitStaff(form: Staff) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/staffs/${props.candId}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  staff.value = {} as Staff;
  await refresh();
  emit("message", message);
}

async function deleteStaff(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch(`/route/items/staffs/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    staffs.value.splice(idx, 1);
  }
  emit("message", message);
}
</script>

<template>
  <UButton
    v-if="props.editable"
    :loading="status == 'pending' || pending"
    :label="
      status == 'pending' || pending
        ? 'Обновление данных...'
        : 'Добавить запись'
    "
    variant="link"
    @click="modal = !modal"
  />
  <UModal v-model="modal" prevent-close>
    <ElementsCardDiv>
      <FormsStaffForm
        :staff="staff"
        @cancel="staff = {}; modal = false"
        @update="submitStaff"
      />
    </ElementsCardDiv>
  </UModal>
  <div v-for="(item, idx) in staffs" :key="idx" class="p-1">
    <ElementsCardDiv>
      <ElementsLabelSlot :label="'Должность'">{{
        item["position"]
      }}</ElementsLabelSlot>
      <ElementsLabelSlot :label="'Департамент'">{{
        item["department"]
      }}</ElementsLabelSlot>
      <template v-if="props.editable" #footer>
        <ElementsNavSimpHoriz
          @delete="deleteStaff(item['id'], idx)"
          @update="
            staff = item;
            modal = true;
          "
        />
      </template>
    </ElementsCardDiv>
  </div>
</template>
