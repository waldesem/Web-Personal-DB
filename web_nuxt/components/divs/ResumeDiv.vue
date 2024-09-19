<script setup lang="ts">
import { useFetchAuth } from "@/utils/auth";
import type { Persons } from "@/types/interfaces";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["update"]);

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
    type: Object,
    default: {} as Persons,
  },
});

const dataResume = ref({
  action: "",
  region: "",
  form: {} as Persons,
});

async function changeRegion(): Promise<void> {
  if (!confirm("Вы действительно хотите изменить регион?")) return;
  const response = await authFetch(`/api/region/${props.candId}`, {
    params: {
      region: dataResume.value.region,
    },
  });
  console.log(response);
  emit("update");
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Информация",
    description: "Изменение региона успешно",
    color: "green",
  });
}

async function deleteItem() {
  if (!confirm(`Вы действительно хотите удалить запись?`)) return;
  const response = await authFetch(`/api/persons/${props.candId}`, {
    method: "DELETE",
  });
  console.log(response);
  toast.add({
    icon: "i-heroicons-information-circle",
    title: "Информация",
    description: `Запись с ID ${props.candId} удалена`,
    color: "primary",
  });
  navigateTo("/persons");
}

function cancelAction() {
  dataResume.value.action = "";
  emit("update");
}
</script>

<template>
  <UCard>
    <div v-if="dataResume.action">
      <FormsResumeForm
        :action="dataResume.action"
        :resume="props.person"
        @cancel="cancelAction"
        @update="emit('update')"
      />
    </div>
    <div v-else>
      <ElementsLabelSlot :label="'Регион'">
        <USelect
          v-model="dataResume.region"
          style="width: 20%"
          :options="[
            'Главный офис',
            'РЦ Юг',
            'РЦ Запад',
            'РЦ Урал',
            'РЦ Восток',
          ]"
          :disabled="!props.editable"
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
        <a
          class="text-primary"
          target="_blank"
          :href="props.person['destination']"
        >
          {{ props.person["destination"] }}
        </a>
      </ElementsLabelSlot>
      <ElementsLabelSlot :label="'Дополнительная информация'">
        {{ props.person["addition"] ? props.person["addition"] : "-" }}
      </ElementsLabelSlot>
    </div>
    <template v-if="props.editable && !dataResume.action" #footer>
      <ElementsNaviHorizont
        :cand-id="props.candId"
        :input-id="'resume-file'"
        :item="'persons'"
        @delete="deleteItem"
        @update="dataResume.action = 'update'"
      />
    </template>
  </UCard>
</template>
