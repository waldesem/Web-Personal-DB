<script setup lang="ts">
import type { Staff } from "@/types";

await preloadComponents("DivsItemsStaffItem");

const authFetch = useFetchAuth();

const candId = inject("candId") as Ref<string>;
const editable = inject("editable") as Ref<boolean>;

const edit = ref(false);
const modal = ref(false);
const pending = ref(false);
const staff = ref({} as Staff);
const staffs = ref<Staff[]>([]);
const index = ref(0);

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
  index.value = 0;
  if (message == "success") {
    staffs.value.splice(idx, 1);
  }
  emitMessage(message);
}
</script>

<template>
  <UCard
    class="my-2 mx-1"
    :class="{ 'animate-pulse': status == 'pending' || pending }"
  >
    <USwitch
      v-if="editable"
      v-model="edit"
      :label="edit ? 'Отключить редактирование' : 'Включить редактирование'"
      size="xs"
      class="mb-2 me-2 justify-end"
    />
    <div v-for="(item, idx) in staffs" :key="idx" class="p-1">
      <UCard>
        <div class="flex">
          <div v-if="edit" class="flex-none mr-6 self-center">
            <input v-model="index" type="radio" name="staff" :value="idx">
          </div>
          <div class="flex-grow">
            <DivsItemsStaffItem :item="item" />
          </div>
        </div>
      </UCard>
    </div>
    <template v-if="edit" #footer>
      <UModal
        v-model:open="modal"
        :dismissible="false"
        title="Должности"
        description="Данные профиля"
      >
        <template #content>
          <UCard>
            <FormsStaffForm
              :staff="staff"
              @cancel="
                staff = {} as Staff;
                modal = false;
              "
              @update="submitStaff"
            />
          </UCard>
        </template>
      </UModal>
      <UButton
        icon="i-heroicons-document-plus"
        label="Добавить"
        variant="ghost"
        @click="
          staff = {} as Staff;
          modal = true;
        "
      />
      <ElementsDivMenu
        v-if="staffs.length > 0"
        @update="
          staff = staffs[index];
          modal = true;
        "
        @delete="deleteStaff(staffs[index].id, index)"
      />
    </template>
  </UCard>
</template>
