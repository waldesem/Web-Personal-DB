<script setup lang="ts">
import type { Address } from "@/types/interfaces";

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
const edit = ref(false);
const itemId = ref("");
const address = ref({} as Address);

const {
  data: addresses,
  refresh,
  status,
} = await useLazyAsyncData("addresses", async () => {
  const response = await authFetch("/api/addresses/" + props.candId);
  return response;
});

async function deleteAddress(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const response = await authFetch("/api/addresses/" + id, {
    method: "DELETE",
  });
  console.log(response);
  toast.add({
    icon: "i-heroicons-information-circle",
    title: "Информация",
    description: `Запись с ID ${id} удалена`,
    color: "primary",
  });
  refresh();
}

async function cancelOperation() {
  closeAction();
  refresh();
}

function closeAction() {
  edit.value = false;
  collapse.value = false;
  itemId.value = "";
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
    <div v-if="collapse" class="p-1">
      <UCard>
        <FormsAddressForm @cancel="cancelOperation" @update="refresh" />
      </UCard>
    </div>
  </Transition>
  <div v-if="addresses && addresses.length">
    <div v-for="(item, idx) in addresses" :key="idx" class="py-3">
      <ElementsSkeletonDiv v-if="status == 'pending'" :rows="8" />
      <UCard v-else>
        <FormsAddressForm
          v-if="edit && itemId == item['id'].toString()"
          :addrs="address"
          @cancel="cancelOperation"
          @update="refresh"
        />
        <div v-else>
          <ElementsLabelSlot :label="'Тип'">{{
            item["view"]
          }}</ElementsLabelSlot>
          <ElementsLabelSlot :label="'Адрес'">{{
            item["addresses"]
          }}</ElementsLabelSlot>
        </div>
        <template
          v-if="props.editable && (!edit || itemId != item['id'].toString())"
          #footer
        >
          <ElementsNaviHorizont
            :navlen="2"
            @delete="deleteAddress(item['id'])"
            @update="
              address = item;
              itemId = item['id'].toString();
              edit = true;
            "
          />
        </template>
      </UCard>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending'" :rows="8" />
    <p v-else class="text-primary">Адреса отсутствуют</p>
  </div>
</template>
