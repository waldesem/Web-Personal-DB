<script setup lang="ts">
import type { Staff } from "@/types/interfaces";

const authFetch = useFetchAuth();

const toast = useToast();

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

const {
  data: staffs,
  refresh,
  status,
} = await useLazyAsyncData("staffs", async () => {
  const response = await authFetch("/api/staffs/" + props.candId);
  return response as Staff[];
});

async function submitStaff(form: Staff) {
  pending.value = true;
  closeAction();
  await authFetch("/api/staffs/" + props.candId, {
    method: "POST",
    body: form,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  pending.value = false;
  refresh();
}

async function deleteStaff(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  await authFetch("/api/staffs/" + id, {
    method: "DELETE",
  });
  toast.add({
    icon: "i-heroicons-information-circle",
    title: "Информация",
    description: `Запись с ID ${id} удалена`,
    color: "primary",
  });
  refresh();
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
