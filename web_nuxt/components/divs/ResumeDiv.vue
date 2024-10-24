<script setup lang="ts">
import type { Persons } from "@/types/interfaces";
import { useDateFormat } from "@vueuse/core";

prefetchComponents(["FormsResumeForm", "ElementsSkeletonDiv"]);

const emit = defineEmits(["update", "message"]);

const toast = useToast();

const authFetch = useFetchAuth();

const props = defineProps({
  status: {
    type: String,
    default: "",
  },
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
const opening = ref(false);

async function changeRegion(): Promise<void> {
  if (!confirm("Вы действительно хотите изменить регион?")) return;
  const { message } = (await authFetch(`/api/region/${props.candId}`, {
    params: {
      region: region.value,
    },
  })) as Record<string, string>;
  if (message == "success") {
    emit("update");
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: "Изменение региона успешно",
      color: "green",
    });
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Регион не был изменен",
      color: "red",
    });
  }
}

async function openFolder() {
  opening.value = true;
  await authFetch("/api/folder/" + props.candId);
  opening.value = false;
}

async function submitResume(form: Persons) {
  pending.value = true;
  edit.value = false;
  const { message } = (await authFetch(`/api/items/persons/${props.candId}`, {
    method: "POST",
    body: form,
  })) as Record<string, string>;
  pending.value = false;
  emit("update");
  emit("message", message);
}

async function deleteItem() {
  pending.value = true;
  const { message } = await authFetch(`/api/items/persons/${props.candId}`, {
    method: "DELETE",
  });
  pending.value = false;
  emit("message", message);
  return navigateTo("/persons");
}

async function cancelAction() {
  edit.value = false;
  emit("update");
}
</script>

<template>
  <ElementsCardDiv>
    <div v-if="edit">
      <FormsResumeForm
        :resume="props.person"
        @cancel="cancelAction"
        @update="submitResume"
      />
    </div>
    <div v-else>
      <ElementsSkeletonDiv v-if="pending || props.status === 'pending'" :rows="14" />
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
            @change="changeRegion"
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
          {{ useDateFormat(props.person["birthday"], "DD.MM.YYYY") }}
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
          {{ useDateFormat(props.person["created"], "DD.MM.YYYY HH:mm") }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Пользователь'">
          {{ props.person["username"] ? props.person["username"] : "" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          v-if="props.person['addition']"
          :label="'Дополнительная информация'"
        >
          {{ props.person["addition"] }}
        </ElementsLabelSlot>
        <ElementsLabelSlot :label="'Материалы'">
          <UButton
            :loading="opening"
            label="Открыть"
            variant="link"
            @click="openFolder"
          />
        </ElementsLabelSlot>
      </div>
    </div>
    <template v-if="props.editable && !edit" #footer>
      <ElementsNaviHorizont
        :cand-id="props.candId"
        item="persons"
        @delete="deleteItem"
        @update="edit = true"
        @upgrade="emit('update')"
      />
    </template>
  </ElementsCardDiv>
</template>
