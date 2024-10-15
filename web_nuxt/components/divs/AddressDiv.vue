<script setup lang="ts">
import type { Address } from "@/types/interfaces";

prefetchComponents(["FormsAddressForm", "ElementsSkeletonDiv"]);

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
const address = ref({} as Address);
const addresses = ref<Address[]>([]);

const { refresh, status } = await useLazyAsyncData("addresses", async () => {
  addresses.value = await authFetch("/api/items/addresses/" + props.candId) as Address[];
});

async function submitAddress(form: Address) {
  pending.value = true;
  closeAction();
  const { message } = (await authFetch("/api/items/addresses/" + props.candId, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  if (message == "success") {
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Успешно",
      description: "Информация обновлена",
      color: "green",
    });
  } else {
    toast.add({
      icon: "i-heroiconsi-heroicons-information-circle",
      title: "Внимание",
      description: "Ошибка при обновлении информации",
      color: "red",
    });
  }
  pending.value = false;
  await refresh();
}

async function deleteAddress(id: string) {
  closeAction();
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const { message } = (await authFetch("/api/items/addresses/" + id, {
    method: "DELETE",
  })) as Record<string, string>;
  if (message == "success") {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Информация",
      description: `Запись с ID ${id} удалена`,
      color: "primary",
    });
    await refresh();
  } else {
    toast.add({
      icon: "i-heroiconsi-heroicons-information-circle",
      title: "Внимание",
      description: "Ошибка при удалении информации",
      color: "red",
    });
  }
}

function cancelOperation() {
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
      <ElementsCardDiv>
        <FormsAddressForm
          :cand-id="props.candId"
          @cancel="cancelOperation"
          @update="submitAddress"
        />
      </ElementsCardDiv>
    </div>
  </Transition>
  <div v-if="addresses && addresses.length">
    <div v-for="(item, idx) in addresses" :key="idx" class="py-3">
      <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
      <ElementsCardDiv v-else>
        <FormsAddressForm
          v-if="edit && itemId == item['id'].toString()"
          :cand-id="props.candId"
          :addrs="address"
          @cancel="cancelOperation"
          @update="submitAddress"
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
      </ElementsCardDiv>
    </div>
  </div>
  <div v-else class="p-3">
    <ElementsSkeletonDiv v-if="status == 'pending' || pending" :rows="8" />
    <p v-else class="text-primary">Адреса отсутствуют</p>
  </div>
</template>
