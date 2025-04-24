<script setup lang="ts">
import type { Staff } from "@/types";

await preloadComponents("DivsItemsStaffItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const modal = ref(false);
const pending = ref(false);
const staff = ref({} as Staff);
const staffs = ref<Staff[]>([]);

const { refresh, status } = await useLazyAsyncData("staffs", async () => {
  staffs.value = (await authFetch(
    "/route/items/staffs/" + candId.value
  )) as Staff[];
});

async function submitStaff(form: Staff) {
  modal.value = false;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/staffs/${candId.value}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  staff.value = {} as Staff;
  await refresh();
  emitMessage(message);
}

async function deleteStaff(id: string, idx: number) {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  pending.value = true;
  const { message } = (await authFetch(`/route/items/staffs/${id}`, {
    method: "DELETE",
  })) as Record<string, string>;
  pending.value = false;
  if (message == "success") {
    staffs.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <ElementsCardDiv>
    <UModal
      v-model:open="modal"
      :dismissible="false"
      title="Должности"
      description="Данные профиля"
    >
      <template #content>
        <ElementsCardDiv>
          <FormsStaffForm
            :staff="staff"
            @cancel="
              staff = {} as Staff;
              modal = false;
            "
            @update="submitStaff"
          />
        </ElementsCardDiv>
      </template>
    </UModal>
    <div v-for="(item, idx) in staffs" :key="idx" class="p-1">
      <ElementsCardDiv>
        <DivsItemsStaffItem :item="item" />
        <template v-if="editable" #footer>
          <ElementsDivMenu
            @delete="deleteStaff(item.id, idx)"
            @update="
              staff = item;
              modal = true;
            "
          />
        </template>
      </ElementsCardDiv>
    </div>
    <template v-if="editable" #footer>
      <div v-if="editable || status == 'pending'" class="my-1">
      <UButton
        :loading="status == 'pending' || pending"
        :label="
          status == 'pending' || pending
            ? 'Обновление данных...'
            : 'Добавить запись'
        "
        variant="ghost"
        icon="i-heroicons-plus-circle"
        @click="modal = !modal"
      />
    </div>
    </template>
  </ElementsCardDiv>
</template>
