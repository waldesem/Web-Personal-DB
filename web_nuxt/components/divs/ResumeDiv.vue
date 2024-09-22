<script setup lang="ts">
import { useFetchAuth } from "@/utils/auth";
import type { Persons } from "@/types/interfaces";

const emit = defineEmits(["update"]);

const toast = useToast();

const authFetch = useFetchAuth();

const props = defineProps({
  editable: {
    type: Boolean,
    default: false,
  },
  candId: {
    type: String,
    default: "",
  },
  person: {
    type: Object as () => Persons,
    default: {} as Persons,
  },
});

const edit = ref(false);
const region = ref("");
const pending = ref(false);

async function changeRegion(): Promise<void> {
  if (!confirm("Вы действительно хотите изменить регион?")) return;
  await authFetch(`/api/region/${props.candId}`, {
    params: {
      region: region.value,
    },
  });
  emit("update");
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: "Изменение региона успешно",
    color: "green",
  });
}

async function openFolder() {
  await authFetch('/api/folder/' + props.candId);
}

function submitResume(form: Persons) {
  pending.value = true;
  edit.value = false;
  authFetch("/api/persons/" + props.candId, {
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
  emit("update");
}

async function deleteItem() {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  await authFetch(`/api/persons/${props.candId}`, {
    method: "DELETE",
  });
  toast.add({
    icon: "i-heroicons-information-circle",
    title: "Информация",
    description: `Запись с ID ${props.candId} удалена`,
    color: "primary",
  });
  navigateTo("/persons");
}

function cancelAction() {
  edit.value = false;
  emit("update");
}
</script>

<template>
  <UCard>
    <div v-if="edit">
      <FormsResumeForm
        :resume="props.person"
        @cancel="cancelAction"
        @update="submitResume"
      />
    </div>
    <div v-else>
      <ElementsSkeletonDiv v-if="pending" :rows="14" />
      <div v-else>
        <ElementsLabelSlot :label="'Регион'">
          <USelect
            v-model="region"
            style="width: 20%"
            :options="[
              'Главный офис',
              'РЦ Юг',
              'РЦ Запад',
              'РЦ Урал',
              'РЦ Восток',
            ]"
            :disabled="!props.editable"
            :placeholder="props.person['region']"
            @change="changeRegion()"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Фамилия'">
          {{ props.person["surname"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Имя'">
          {{ props.person["firstname"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Отчество'">
          {{ props.person["patronymic"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата рождения'">
          {{
            new Date(String(props.person["birthday"])).toLocaleDateString("ru-RU")
          }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Место рождения'">
          {{ props.person["birthplace"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Гражданство'">
          {{ props.person["citizenship"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="props.person['dual']"
          :label="'Двойное гражданство'"
        >
          {{ props.person["dual"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'СНИЛС'">
          {{ props.person["snils"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'ИНН'">
          {{ props.person["inn"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Семейное положение'">
          {{ props.person["marital"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дата записи'">
          {{
            props.person["created"]
              ? new Date(props.person["created"] + " UTC").toLocaleString("ru-RU")
              : ""
          }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Пользователь'">
          {{ props.person["username"] ? props.person["username"] : "" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Материалы'">
          <UButton
            :label="props.person['destination']"
            variant="link"
            @click="openFolder"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Дополнительная информация'">
          {{ props.person["addition"] ? props.person["addition"] : "-" }}
        </ElementsLabelSlot>
      </div>
    </div>
    <template v-if="props.editable && !edit" #footer>
      <ElementsNaviHorizont
        :cand-id="props.candId"
        :input-id="'resume-file'"
        :item="'persons'"
        @delete="deleteItem"
        @update="edit = true"
      />
    </template>
  </UCard>
</template>
